from dataclasses import dataclass
from inspect import Parameter, Signature
from typing import Annotated, Any, Literal, Optional, get_args, get_origin
from pydantic import BaseModel
from datetime import date


class ProcedureInputInfo:
    type: str
    name: str

    def get_TextInputOptions(self: Any):
        try:
            return TextInputOptions(self.must_match_options, self.static_options, self.db_options, self.dynamic_options_name)
        except AttributeError:
            return None


class ProcedureOutputInfo:
    type: str
    name: str


class NumberInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, placeholder: str | None = None, display_format=""):
        super().__init__()
        self.type = "number"
        self.required = required
        self.readonly = readonly
        self.trigger_update = trigger_update
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.placeholder = placeholder
        self.display_format = display_format


class DateInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "date"
        self.required = required
        self.readonly = readonly
        self.trigger_update = trigger_update
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip


class DbOptions:
    def __init__(self, *, connection_name: str, schema: str, table: str, column: str, group_column="", live_filter: Literal["contains"] | Literal["prefix"] | Literal["word_prefix"] = "contains"):
        self.connection_name = connection_name
        self.schema = schema
        self.table = table
        self.column = column
        self.group_column = group_column
        self.live_filter = live_filter


@dataclass
class TextInputOptions:
    must_match_options: bool
    static_options: list[str] | None
    db_options: DbOptions | None
    dynamic_options_name: str


class TextInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, placeholder: str | None = None, multiline = False, must_match_options=False, static_options: list[str] | None = None, db_options: DbOptions | None = None, dynamic_options_output_name: str = ""):
        super().__init__()
        self.type = "text"
        self.required = required
        self.readonly = readonly
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.placeholder = placeholder
        self.multiline = multiline
        self.trigger_update = trigger_update
        self.must_match_options = must_match_options
        self.static_options = static_options
        self.db_options = db_options
        self.dynamic_options_name = dynamic_options_output_name


class TextListInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, must_match_options=False, static_options: list[str] | None = None, db_options: DbOptions | None = None, dynamic_options_output_name: str = ""):
        super().__init__()
        self.type = "textlist"
        self.required = required
        self.readonly = readonly
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.trigger_update = trigger_update
        self.must_match_options = must_match_options
        self.static_options = static_options
        self.db_options = db_options
        self.dynamic_options_name = dynamic_options_output_name


class BooleanInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "boolean"
        self.required = required
        self.readonly = readonly
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.trigger_update = trigger_update


class FilePathInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, file_types: list[str], sample_file_names: list[str] | None = None):
        super().__init__()
        self.type = "filepath"
        self.required = required
        self.readonly = readonly
        self.trigger_update = trigger_update
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.file_types = file_types
        self.sample_file_names = sample_file_names


class FilePathsInput(ProcedureInputInfo):
    def __init__(self, *, required=True, readonly=False, trigger_update=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, file_types: list[str], sample_file_names: list[str] | None = None):
        super().__init__()
        self.type = "filepaths"
        self.required = required
        self.readonly = readonly
        self.trigger_update = trigger_update
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.file_types = file_types
        self.sample_file_names = sample_file_names


class TableInput(ProcedureInputInfo):
    def __init__(self, required=True, readonly=False, label: str | None = None, show_label: bool = True, tooltip: str | None = None, can_add_rows=True, can_delete_rows=True):
        super().__init__()
        self.type = "table"
        self.required = required
        self.readonly = readonly
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.can_add_rows = can_add_rows
        self.can_delete_rows = can_delete_rows
        self.columns = []

    columns: list[ProcedureInputInfo]


class NumberOutput(ProcedureOutputInfo):
    def __init__(self, *, label: str | None = None, show_label: bool = True, tooltip: str | None = None, display_format=""):
        super().__init__()
        self.type = "number"
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.display_format = display_format


class DateOutput(ProcedureOutputInfo):
    def __init__(self, label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "date"
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip


class BooleanOutput(ProcedureOutputInfo):
    def __init__(self, label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "boolean"
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip


class TextOutput(ProcedureOutputInfo):
    def __init__(self, label: str | None = None, show_label: bool = True, tooltip: str | None = None, multiline = False, preformatted = False):
        super().__init__()
        self.type = "text"
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip
        self.multiline = multiline
        self.preformatted = preformatted


class FilePathOutput(ProcedureOutputInfo):
    def __init__(self, *, file_types: list[str], label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "filepath"
        self.file_types = file_types
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip


class FilePathsOutput(ProcedureOutputInfo):
    def __init__(self, *, file_types: list[str], label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "filepaths"
        self.file_types = file_types
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip


class TableOutput(ProcedureOutputInfo):
    def __init__(self, label: str | None = None, show_label: bool = True, tooltip: str | None = None):
        super().__init__()
        self.type = "table"
        self.columns = []
        self.label = label
        self.show_label = show_label
        self.tooltip = tooltip

    columns: list[ProcedureOutputInfo]

def _get_parameter_type(p: Parameter):
    if get_origin(p.annotation) is Annotated:
        inputs_type, _ = get_args(p.annotation)
    else:
        inputs_type = p.annotation
    return inputs_type

def _get_input_meta(field_info):
    f_type = field_info.annotation
    if field_info.metadata:
        for m in field_info.metadata:
            if isinstance(m, ProcedureInputInfo):
                return m
    if f_type == Optional[float]:
        return NumberInput()
    elif f_type == Optional[date]:
        return DateInput()
    elif f_type == Optional[bool]:
        return BooleanInput()
    elif f_type == str:
        return TextInput()
    elif f_type == Optional[list[str]]:
        return TextListInput()
    elif get_origin(f_type) is list:
        f_row_type, *others = get_args(f_type)
        if len(others) == 0 and issubclass(f_row_type, BaseModel):
            return TableInput()
    return None

def _process_input_field_type(model_name, f_meta: ProcedureInputInfo, f_type, errors: list[str]):
    f_name = f_meta.name
    if isinstance(f_meta, TableInput):
        if get_origin(f_type) is list:
            f_row_type, *others = get_args(f_type)
            if len(others) == 0 and issubclass(f_row_type, BaseModel):
                _set_table_input_columns(f_meta, f_row_type, errors)
            else:
                errors.append(
                    f"The type for input field {model_name}.{f_name} should be list[sub_class_of_BaseModel] because it is annotated with TableInput")
        else:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be list[sub_class_of_BaseModel] because it is annotated with TableInput")
    elif isinstance(f_meta, NumberInput):
        if f_type != Optional[float]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be float | None instead of {f_type} because it is annotated with NumberInput")
    elif isinstance(f_meta, DateInput):
        if f_type != Optional[date]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be date | None instead of {f_type} because it is annotated with DateInput")
    elif isinstance(f_meta, BooleanInput):
        if f_type != Optional[bool]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be bool | None instead of {f_type} because it is annotated with BooleanInput")
    elif isinstance(f_meta, TextInput):
        if f_type != str and f_type != str | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be str instead of {f_type} because it is annotated with TextInput")
    elif isinstance(f_meta, TextListInput):
        if f_type != str:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be list[str] | None instead of {f_type} because it is annotated with TextListInput")
    elif isinstance(f_meta, FilePathInput):
        if f_type != str and f_type != str | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be str instead of {f_type} because it is annotated with FilePathInput")
    elif isinstance(f_meta, FilePathsInput):
        if f_type != list[str] | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be list[str] | None instead of {f_type} because it is annotated with FilePathsInput")
    else:
        raise ValueError(f"Input of type {type(f_meta)} was encountered in {model_name}.{f_name} but it is not yet supported")


def _process_output_field_type(model_name: str, f_meta: ProcedureOutputInfo, f_type, errors: list[str]):
    f_name = f_meta.name
    if isinstance(f_meta, TableOutput):
        if get_origin(f_type) is list:
            f_row_type, *others = get_args(f_type)
            if len(others) == 0 and issubclass(f_row_type, BaseModel):
                _set_table_output_columns(f_meta, f_row_type, errors)
            else:
                errors.append(
                    f"The type for output field {model_name}.{f_name} should be list[sub_class_of_BaseModel] because it is annotated with TableOutput")
        else:
            errors.append(
                f"The type for output field {model_name}.{f_name} should be list[sub_class_of_BaseModel] because it is annotated with TableOutput")
    elif isinstance(f_meta, NumberOutput):
        if f_type != Optional[float]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be float | None instead of {f_type} because it is annotated with NumberOutput")
    elif isinstance(f_meta, DateOutput):
        if f_type != Optional[date]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be date | None instead of {f_type} because it is annotated with DateOutput")
    elif isinstance(f_meta, BooleanOutput):
        if f_type != Optional[bool]:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be bool | None instead of {f_type} because it is annotated with BooleanOutput")
    elif isinstance(f_meta, TextOutput):
        if f_type != str and f_type != str | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be str instead of {f_type} because it is annotated with TextOutput")
    elif isinstance(f_meta, FilePathOutput):
        if f_type != str and f_type != str | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be str instead of {f_type} because it is annotated with FilePathOutput")
    elif isinstance(f_meta, FilePathsOutput):
        if f_type != list[str] | None:
            errors.append(
                f"The type for input field {model_name}.{f_name} should be list[str] | None instead of {f_type} because it is annotated with FilePathsOutput")
    else:
        raise ValueError(f"Input of type {type(f_meta)} was encountered in {model_name}.{f_name} is not yet supported")

def _get_output_meta(field_info):
    f_type = field_info.annotation
    if field_info.metadata:
        for m in field_info.metadata:
            if isinstance(m, ProcedureOutputInfo):
                return m
    if f_type == Optional[float]:
        return NumberOutput()
    elif f_type == Optional[date]:
        return DateOutput()
    elif f_type == Optional[bool]:
        return BooleanOutput()
    elif f_type == str:
        return TextOutput()
    elif get_origin(f_type) is list:
        f_row_type, *others = get_args(f_type)
        if len(others) == 0 and issubclass(f_row_type, BaseModel):
            return TableOutput()
    return None

def _set_table_input_columns(input: TableInput, row_type: type[BaseModel], errors: list[str]):
    fields = row_type.model_fields
    for f_name, f_info in fields.items():
        f_type = f_info.annotation
        f_meta = _get_input_meta(f_info)
        if f_meta:
            f_meta.name = f_name
            _process_input_field_type(row_type.__name__, f_meta, f_type, errors)
            input.columns.append(f_meta)
        else:
            errors.append(f"No metadata found for field {f_name} of input field {
                          input.name} and its type is not one of the supported types for which metadata can be inferred")


def _set_table_output_columns(output: TableOutput, row_type: type[BaseModel], errors: list[str]):
    fields = row_type.model_fields
    for f_name, f_info in fields.items():
        f_type = f_info.annotation
        f_meta = _get_output_meta(f_info)
        if f_meta:
            f_meta.name = f_name
            _process_output_field_type(row_type.__name__, f_meta, f_type, errors)
            output.columns.append(f_meta)
        else:
            errors.append(f"No metadata found for field {f_name} of input field {
                          output.name} and its type is not one of the supported types for which metadata can be inferred")

class ProcedurePageRunButton:
    def __init__(self):
        self.label = None

    label: str | None

class ProcedurePageInfo:
    def __init__(self) -> None:
        self.run_button = ProcedurePageRunButton()

    run_button: ProcedurePageRunButton

class ProcedureInfo:
    def __init__(self, proc_sig: Signature, *, unique_id: str, name: str, group: str, version: int, immediate, inputs_require_initialization, page_info: ProcedurePageInfo | None):
        self.reg_id = None
        self.reg_version = None
        self.unique_id = unique_id.lower()
        self.name = name
        self.group = group
        self.version = version
        self.immediate = immediate
        self.inputs_require_initialization = inputs_require_initialization

        self.errors = []
        self.inputs = []
        self.outputs = []

        self.page_info = page_info
        
        dyn_output_names: set[str] = set()
        for k, p in proc_sig.parameters.items():
            if k == 'inputs':
                inputs_type = _get_parameter_type(p)
                if issubclass(inputs_type, BaseModel):
                    fields = inputs_type.model_fields
                    for f_name, f_info in fields.items():
                        f_type = f_info.annotation
                        f_meta = _get_input_meta(f_info)
                        if f_meta:
                            f_meta.name = f_name
                            f_topts = f_meta.get_TextInputOptions()
                            if f_topts is not None and f_topts.dynamic_options_name:
                                dyn_output_names.add(f_topts.dynamic_options_name)
                            _process_input_field_type(inputs_type.__name__, f_meta, f_type, self.errors)
                            self.inputs.append(f_meta)
                        else:
                            self.errors.append(
                                f"No metadata found for input field {f_name} and its type is not one of the supported types for which metadata can be inferred")
                else:
                    self.errors.append('The type of the inputs argument should be a subclass of BaseModel')
        outputs_type = proc_sig.return_annotation
        if outputs_type is Signature.empty:
            self.errors.append(
                'The procedure must have an explicitly annotated return type')
        elif outputs_type is not None:
            if issubclass(outputs_type, BaseModel):
                fields = outputs_type.model_fields
                for f_name, f_info in fields.items():
                    if f_name in dyn_output_names:
                        continue
                    f_type = f_info.annotation
                    f_meta = _get_output_meta(f_info)
                    if f_meta:
                        f_meta.name = f_name
                        _process_output_field_type(outputs_type.__name__, f_meta, f_type, self.errors)
                        self.outputs.append(f_meta)
                    else:
                        self.errors.append(
                            f"No metadata found for output field {f_name} and its type is not one of the supported types for which metadata can be inferred")
            else:
                self.errors.append(
                    'The output type of the procedure must be a subclass of BaseModel')

    reg_id: int
    reg_version: int
    unique_id: str
    name: str
    group: str
    version: int
    immediate: bool
    inputs_require_initialization: bool

    inputs: list[ProcedureInputInfo]
    outputs: list[ProcedureOutputInfo]
    errors: list[str]
