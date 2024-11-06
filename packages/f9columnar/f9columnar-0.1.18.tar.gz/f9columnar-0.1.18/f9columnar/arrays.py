from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Dict, List

import awkward as ak
import numpy as np

from f9columnar.processors import Processor
from f9columnar.utils.ak_helpers import check_list_type, check_numpy_type


@dataclass
class BaseArrays:
    array: ak.Array
    fields: List[str] = dataclass_field(default_factory=list)

    def __post_init__(self):
        self.fields = self.array.fields

    @property
    def shape(self):
        return (len(self.array), len(self.fields))

    def mask(self, mask, inplace=True):
        if inplace:
            self.array = self.array[mask]
            return self
        else:
            return self.array[mask]

    def _check_type(self, array):
        raise NotImplementedError

    def __setitem__(self, field, new_array):
        if not self._check_type(new_array):
            raise ValueError(f"Field {field} is not of the correct type!")

        self.array[field] = new_array
        self.fields.append(field)

        return self

    def __getitem__(self, value):
        if type(value) is str:
            return self.array[value]
        elif type(value) is int:
            return self.array[value]
        elif type(value) is ak.Array or type(value) is np.ndarray:
            return self.mask(value)
        elif type(value) is slice:
            return self.array[value]
        else:
            raise ValueError("Value must be a field name or an array mask!")

    def __len__(self):
        return len(self.array)

    def __delitem__(self, field):
        self.array = ak.without_field(self.array, field)
        self.fields.remove(field)
        return self


@dataclass
class FlatArrays(BaseArrays):
    def _check_type(self, array):
        return check_numpy_type(array)

    def __str__(self):
        return f"{self.__class__.__name__}(shape={self.shape})"


@dataclass
class JaggedArrays(BaseArrays):
    def _check_type(self, array):
        return check_list_type(array)

    def _get_non_empty_mask(self):
        return ak.num(self.array[self.fields[0]]) > 0

    def remove_empty(self):
        mask = self._get_non_empty_mask()
        self.mask(mask, inplace=True)
        return self

    def __str__(self):
        return f"{self.__class__.__name__}(shape={self.shape})"


@dataclass
class Arrays:
    """This class is used to store flat and jagged arrays separately. It is used to store awkward arrays in a more
    structured way. It is initialized in the `ArrayProcessor` to separate flat and jagged fields. The funconality is
    similar to `ak.Array` but with seperate handling of flat and jagged arrays. It is intended to make it easier to
    work with ntuples that contain both flat (e.g. MC weights) and jagged fields (e.g. pt).

    Parameters
    ----------
    flat_arrays : FlatArrays
        Flat arrays.
    jagged_arrays : JaggedArrays
        Jagged arrays.

    Other Parameters
    ----------------
    flat_fields : list
        List of flat fields.
    jagged_fields : list
        List of jagged fields.
    fields : list
        List of all fields.

    Attributes
    ----------
    shape : tuple
        Shape of the arrays (number of events, number of flat array, number of jagged arrays).

    Methods
    -------
    update_fields()
        Update flat and jagged fields on (or after) initialization.
    mask_flat(mask, inplace=True)
        Mask flat arrays.
    mask_jagged(mask, inplace=True)
        Mask jagged arrays.
    remove_empty(inplace=True, return_mask=False)
        Remove empty sub arrays.

    Warning
    -------
    Masking is done inplace by default using `__setitem__`. To return a masked array, set `inplace=False` and use
    `mask_flat` or `mask_jagged` methods.

    Note
    ----
    To delete a field, use `del arrays[field]` syntax.

    """

    flat_arrays: FlatArrays | None = None
    jagged_arrays: JaggedArrays | None = None

    flat_fields: List[str] = dataclass_field(default_factory=list)
    jagged_fields: List[str] = dataclass_field(default_factory=list)
    fields: List[str] = dataclass_field(default_factory=list)

    def __post_init__(self):
        self.update_fields()

    def update_fields(self):
        self.fields = []

        if self.flat_arrays is not None:
            self.flat_fields = self.flat_arrays.fields
            self.fields += self.flat_fields

        if self.jagged_arrays is not None:
            self.jagged_fields = self.jagged_arrays.fields
            self.fields += self.jagged_fields

        return self

    @property
    def shape(self):
        return (len(self), len(self.flat_fields), len(self.jagged_fields))

    def mask_flat(self, mask, inplace=True):
        if inplace:
            if self.flat_arrays is not None:
                self.flat_arrays.mask(mask, inplace=True)

            if self.jagged_arrays is not None:
                self.jagged_arrays.mask(mask, inplace=True)

            return self
        else:
            flat_masked, jagged_masked = None, None

            if self.flat_arrays is not None:
                flat_masked = self.flat_arrays.mask(mask, inplace=False)

            if self.jagged_arrays is not None:
                jagged_masked = self.jagged_arrays.mask(mask, inplace=False)

            return flat_masked, jagged_masked

    def mask_jagged(self, mask, inplace=True):
        if inplace:
            if self.jagged_arrays is not None:
                self.jagged_arrays.mask(mask, inplace=True)

            return self
        else:
            jagged_masked = None

            if self.jagged_arrays is not None:
                jagged_masked = self.jagged_arrays.mask(mask, inplace=False)

            return jagged_masked

    def remove_empty(self, inplace=True, return_mask=False):
        if self.jagged_arrays is None:
            if return_mask:
                return None
            else:
                return self

        non_empty_mask = self.jagged_arrays._get_non_empty_mask()

        if return_mask:
            return non_empty_mask
        else:
            return self.mask_flat(non_empty_mask, inplace=inplace)

    def __setitem__(self, field, new_array):
        if check_numpy_type(new_array):
            if self.flat_arrays is None:
                self.flat_arrays = FlatArrays(ak.Array({field: new_array}))
            else:
                self.flat_arrays[field] = new_array

        elif check_list_type(new_array):
            if self.jagged_arrays is None:
                self.jagged_arrays = JaggedArrays(ak.Array({field: new_array}))
            else:
                self.jagged_arrays[field] = new_array

        else:
            raise ValueError("Array is not of the correct type!")

        self.update_fields()

        return self

    def _get_by_field(self, field):
        if field in self.flat_fields:
            return self.flat_arrays[field]
        elif field in self.jagged_fields:
            return self.jagged_arrays[field]
        else:
            raise KeyError(f"Field {field} not found in flat or jagged fields!")

    def _get_by_slice(self, slice_idx):
        return self.flat_arrays[slice_idx], self.jagged_arrays[slice_idx]

    def _get_by_mask(self, mask):
        if check_numpy_type(mask):
            self.mask_flat(mask, inplace=True)
        elif check_list_type(mask):
            self.mask_jagged(mask, inplace=True)
        else:
            raise ValueError("Mask is not of the correct type!")

        return self

    def __getitem__(self, value):
        if type(value) is str:
            return self._get_by_field(value)
        elif type(value) is int:
            return self._get_by_slice(value)
        elif type(value) is ak.Array or type(value) is np.ndarray:
            return self._get_by_mask(value)
        elif type(value) is slice:
            return self._get_by_slice(value)
        else:
            raise ValueError("Value must be a field name, int, array mask or slice!")

    def __len__(self):
        if self.flat_arrays is None and self.jagged_arrays is not None:
            return len(self.jagged_arrays)
        elif self.flat_arrays is not None and self.jagged_arrays is None:
            return len(self.flat_arrays)
        elif self.flat_arrays is None and self.jagged_arrays is None:
            return np.nan
        else:
            len_flat, len_jagged = len(self.flat_arrays), len(self.jagged_arrays)
            assert len_flat == len_jagged, "Flat and jagged arrays have different lengths!"
            return len_flat

    def __delitem__(self, field):
        if field in self.flat_fields:
            del self.flat_arrays[field]
        elif field in self.jagged_fields:
            del self.jagged_arrays[field]
        else:
            raise KeyError(f"Field {field} not found in flat or jagged fields!")

        self.fields.remove(field)

        if self.flat_arrays is not None and len(self.flat_arrays.fields) == 0:
            self.flat_arrays = None

        if self.jagged_arrays is not None and len(self.jagged_arrays.fields) == 0:
            self.jagged_arrays = None

        return self

    def __str__(self):
        return f"{self.__class__.__name__}(shape={self.shape})"


@dataclass
class GroupArrays:
    group_arrays: dict

    group_field_map: Dict[str, List[str]] = dataclass_field(default_factory=dict)
    field_group_map: Dict[str, str] = dataclass_field(default_factory=dict)

    groups: List[str] = dataclass_field(default_factory=list)
    fields: List[str] = dataclass_field(default_factory=list)

    def __post_init__(self):
        self.update_fields()

    def update_fields(self):
        self.group_field_map, self.field_group_map = {}, {}

        for group, arrays in self.group_arrays.items():
            fields = arrays.fields
            self.group_field_map[group] = fields

            for field in fields:
                self.field_group_map[field] = group

        self.groups = list(self.group_arrays.keys())
        self.fields = list(self.field_group_map.keys())

    def remove_empty(self, group=None, inplace=True, return_mask=False):
        non_empty_masks = []

        if group is None:
            for arrays in self.group_arrays.values():
                non_empty_mask = arrays.remove_empty(inplace=inplace, return_mask=True)

                if non_empty_mask is not None:
                    non_empty_masks.append(non_empty_mask)

            non_empty_mask = non_empty_masks.pop(0)
            for mask in non_empty_masks:
                non_empty_mask = non_empty_mask & mask
        else:
            non_empty_mask = self.group_arrays[group].remove_empty(inplace=inplace, return_mask=True)

        for group in self.group_arrays.keys():
            self.group_arrays[group].mask_flat(non_empty_mask, inplace=True)

        if return_mask:
            return non_empty_mask
        else:
            return self

    def __setitem__(self, value, new_array):
        if type(value) is tuple:
            group, field = value
        else:
            group, field = "other", value

        if type(new_array) is Arrays:
            self.group_arrays[field] = new_array
            self.update_fields()
            return self

        if group not in self.groups:
            arrays_handler = ArraysHandler()

            if type(new_array) is np.ndarray:
                new_array = ak.Array({field: new_array})

            self.group_arrays[group] = arrays_handler.make_arrays(new_array)
        else:
            arrays = self.group_arrays[group]
            arrays[field] = new_array
            self.group_arrays[group] = arrays

        self.update_fields()

        return self

    def __getitem__(self, value):
        if type(value) is tuple:
            value, other_value = value
        else:
            other_value = None

        if type(value) is not str:
            for group, arrays in self.group_arrays.items():
                self.group_arrays[group] = arrays[value]

            return self

        group, field = None, None

        if value in self.groups:
            group = value
        elif value in self.fields:
            field = value
        else:
            raise KeyError(f"Group or field {value} not found!")

        if group and not other_value:
            arrays = self.group_arrays[group]
        elif group and other_value:
            arrays = self.group_arrays[group][other_value]
        elif field and not other_value:
            group = self.field_group_map[field]
            arrays = self.group_arrays[group][field]
        elif field and other_value:
            group = self.field_group_map[field]
            arrays = self.group_arrays[group][field][other_value]
        else:
            raise ValueError("Invalid input!")

        return arrays

    def __delitem__(self, value):
        assert value in self.groups or value in self.fields, f"Group or field {value} not found!"

        if value in self.fields:
            group = self.field_group_map[value]
            del self.group_arrays[group][value]

        if value in self.groups:
            del self.group_arrays[value]
            self.update_fields()

        return self

    def __len__(self):
        len_lst = []

        for arrays in self.group_arrays.values():
            len_lst.append(len(arrays))

        # a hard requirement for group arrays
        assert len(set(len_lst)) == 1, "Groups have different number of events!"

        return len_lst[0]

    def __str__(self):
        return f"{self.__class__.__name__}(groups={self.groups})"


class ArraysHandler:
    @staticmethod
    def _get_fields(arrays):
        arrays_contents = arrays.type.content.contents
        arrays_fields = arrays.type.content.fields

        flat_fields, jagged_fields, other_fields = [], [], []

        for content, array_field in zip(arrays_contents, arrays_fields):
            if isinstance(content, ak.types.NumpyType):
                flat_fields.append(array_field)
            elif isinstance(content, ak.types.ListType):
                jagged_fields.append(array_field)
            else:
                other_fields.append(array_field)

        return flat_fields, jagged_fields, other_fields

    def make_arrays(self, arrays):
        flat_fields, jagged_fields, _ = self._get_fields(arrays)

        flat_arrays, jagged_arrays = None, None

        if len(flat_fields) != 0:
            flat_arrays = arrays[flat_fields]
            flat_arrays = FlatArrays(flat_arrays)

        if len(jagged_fields) != 0:
            jagged_arrays = arrays[jagged_fields]
            jagged_arrays = JaggedArrays(jagged_arrays)

        arrays = Arrays(flat_arrays=flat_arrays, jagged_arrays=jagged_arrays)

        return arrays

    def make_array_groups(self, arrays, groups):
        fields = arrays.fields

        group_arrays_dct, all_group_fields = {}, []

        for group in groups:
            group_fields = [field for field in fields if field.startswith(f"{group}_")]
            all_group_fields += group_fields

            group_arrays = arrays[group_fields]
            group_arrays_dct[group] = self.make_arrays(group_arrays)

        non_group_fields = list(set(fields) - set(all_group_fields))

        if len(non_group_fields) != 0:
            non_group_arrays = arrays[non_group_fields]
            group_arrays_dct["other"] = self.make_arrays(non_group_arrays)

        arrays = GroupArrays(group_arrays=group_arrays_dct)

        return arrays


class ArrayProcessor(Processor):
    def __init__(self, groups=None):
        """Processor to separate flat and jagged fields into two arrays from an awkward array.

        Note
        ----
        This will modify the input arrays. It is intended to be used as the first processor in the analysis chain in
        the case of ntuples that contain both flat and jagged fields.

        """
        super().__init__(name="arrayProcessor")
        assert groups is None or isinstance(groups, list), "Groups must be a list of strings or None!"
        self.groups = groups

        self.arrays_handler = ArraysHandler()

    def run(self, arrays):
        if self.groups is None:
            arrays = self.arrays_handler.make_arrays(arrays)
        else:
            arrays = self.arrays_handler.make_array_groups(arrays, self.groups)

        return {"arrays": arrays}
