"""Module for outputting results of timeseries comparisons.

Currently this module only contains classes for writing comparisons between
IAM model results and harmonisation data or other timeseries reference data.
"""
from collections.abc import Sequence, Mapping, Callable
import typing as tp
import warnings

import pandas as pd
from pandas.io.formats.style import Styler as PandasStyler
import pyam

from ..targets.target_classes import (
    CriterionTargetRange,
    RelativeRange,
)
from ..criteria.timeseries_criteria_core import (
    TimeseriesRefCriterion,
)
from ..criteria.timeseries_criteria_core import DIM
from .base import (
    CTCol,
    CriterionTargetRangeOutput,
    DataFrameMappingWriterTypeVar,
    NoWriter,
    ResultOutput,
    StyledResultOutput,
    WriteReturnTypeVar,
    WriterTypeVar,
    CriterionTargetRangeOutputStyles,
)
from .excel import (
    ExcelFileSpec,
    MultiDataFrameExcelWriter,
    ExcelWriterBase,
)
from ..type_helpers import not_none


TimeseriesRefCriterionTypeVar = tp.TypeVar(
    'TimeseriesRefCriterionTypeVar',
    bound=TimeseriesRefCriterion,
)  # Should probably also add `covariant=True`, but need to check with actual
   # behavior whether it's that or `contravariant=True`.

CriterionTargetRangeTypeVar = tp.TypeVar(
    'CriterionTargetRangeTypeVar',
    bound=CriterionTargetRange,
)

SummaryOutputTypeVar = tp.TypeVar(
    'SummaryOutputTypeVar',
    bound=CriterionTargetRangeOutput,
)

class TimeseriesRefFullComparisonOutput(
    ResultOutput[
        TimeseriesRefCriterionTypeVar,
        pyam.IamDataFrame,
        pd.DataFrame,
        WriterTypeVar,
        WriteReturnTypeVar,
    ]
):
    """Class for outputting full timeseries data from timeseries comparisons.

    The `prepare_output` method of this class takes a `TimeseriesRefCriterion`
    or subclass instance as input, and returns output as a pandas `DataFrame`.
    The `DataFrame` returned by this class is the same as one would get by
    pivoting/unstacking the years of the Series returned by the `get_values`
    method of the `TimeseriesRefCriterion` instance, or by creating a
    `pyam.IamDataFrame` from that Serie` and calling its `.timeseries()` method.
    Subclasses may implement more case-specific behavior and processing.
    """

    def prepare_output(
        self,
        data: pyam.IamDataFrame,
        /,
        criteria: tp.Optional[TimeseriesRefCriterionTypeVar] = None,
    ) -> pd.DataFrame:
        """Prepare the output data for writing.

        Parameters
        ----------
        criterion : TimeseriesRefCriterion
            The criterion to be used to prepare the output data.

        Returns
        -------
        pd.DataFrame
            The output data to be written.
        """
        if criteria is None:
           criteria = self.criteria
        comparison_result: pd.Series = criteria.compare(data)
        timeseries_df: pd.DataFrame = \
            comparison_result.unstack(level=DIM.TIME)
        return timeseries_df
    ###END def TimeseriesComparisonFullDataOutput.prepare_output

###END class TimeseriesComparisonFullDataOutput


class CriterionTargetRangeOtherKwargs(tp.TypedDict, total=False):
    """Additional keyword arguments to be passed to the
    `CriterionTargetRange` class, except for the `target`, `range` and
    `distance_func` parameters.

    Used to annotate the `criterion_target_range_kwargs` parameter of the
    `TimeSeriesRefFullAndSummaryOutput` class `__init__` method.
    """
    unit: tp.Optional[str]
    name: tp.Optional[str]
    convert_value_units: tp.Optional[bool]
    convert_input_units: bool
    value_unit: tp.Optional[str]
###END class TypedDict CriterionTargetRangeOtherKwargs


TimeseriesOutputTypeVar = tp.TypeVar(
    'TimeseriesOutputTypeVar',
    bound=TimeseriesRefFullComparisonOutput,
)
CTRangeOutputStyleTypeVar = tp.TypeVar(
    'CTRangeOutputStyleTypeVar',
    bound=CriterionTargetRangeOutputStyles,
)


class MissingDefaultTypeError(Exception):
    """Exception raised when a default type is missing.

    Used by the `TimeseriesRefFullAndSummaryOutput` class `__init__` method
    when `target_range`, `timeseries_output` or `summary_output` is not set,
    and the class attributes `target_range_default_type`,
    `timeseries_output_default_type` or `summary_output_default_type`,
    respectively, is not defined (i.e., the `__init__` method is being called
    on `TimeseriesRefFullAndSummaryOutput` itself or on a subclass that does not
    define these class attributes).
    """
    ...
###END class MissingDefaultTypeError


class TimeseriesRefComparisonAndTargetOutput(
    tp.Generic[
        TimeseriesRefCriterionTypeVar,
        CriterionTargetRangeTypeVar,
        TimeseriesOutputTypeVar,
        SummaryOutputTypeVar,
        DataFrameMappingWriterTypeVar,
        WriteReturnTypeVar,
        CTRangeOutputStyleTypeVar,
    ],
    StyledResultOutput[
        TimeseriesRefCriterionTypeVar,
        pyam.IamDataFrame,
        dict[str, pd.DataFrame],
        DataFrameMappingWriterTypeVar | NoWriter,
        WriteReturnTypeVar,
        CTRangeOutputStyleTypeVar|None,
        dict[str, PandasStyler],
    ]
):
    """Base class to output full comparison and targets for TimeseriesRefCriterion.

    The `prepare_output` method of this class returns a two-element dictionary,
    one with the full data as prepared by a `TimeseriesComparisonFullDataOutput`
    instance, and the second with summary metrics prepared by a instance of
    `CriterionTargetRangeOutput` or subclass.

    The class is intended to be used for outputting full and summary results to
    different worksheets in an Excel file using `MultiDataFrameExcelWriter`. The
    keys of the dictionary are then the names of the worksheets. But it can
    also be used for any other writer or purpose that accepts a two-element
    dictionary of the type described here.
    """

    target_range_default_type: tp.Type[CriterionTargetRangeTypeVar]
    timeseries_output_default_type: tp.Type[TimeseriesOutputTypeVar]
    summary_output_default_type: tp.Type[SummaryOutputTypeVar]

    def __init__(
            self,
            *,
            criteria: tp.Optional[TimeseriesRefCriterionTypeVar] = None,
            target_range: tp.Optional[
                Callable[
                    [TimeseriesRefCriterionTypeVar],
                    CriterionTargetRangeTypeVar
                ] | CriterionTargetRangeTypeVar
            ] = None,
            target_range_type: tp.Optional[
                tp.Type[CriterionTargetRangeTypeVar]
            ] = None,
            target: tp.Optional[float] = None,
            range: tp.Optional[tuple[float, float] | RelativeRange] = None,
            distance_func: tp.Optional[Callable[[float], float]] = None,
            timeseries_output: tp.Optional[
                tp.Callable[
                    [TimeseriesRefCriterion],
                    TimeseriesOutputTypeVar,
                ]
            ] = None,
            timeseries_output_type: tp.Optional[
                tp.Type[TimeseriesOutputTypeVar]
            ] = None,
            summary_output: tp.Optional[
                tp.Callable[
                    [CriterionTargetRangeTypeVar],
                    SummaryOutputTypeVar,
                ]
            ] = None,
            summary_output_type: tp.Optional[
                tp.Type[SummaryOutputTypeVar]
            ] = None,
            writer: tp.Optional[DataFrameMappingWriterTypeVar] = None,
            style: tp.Optional[CTRangeOutputStyleTypeVar] = None,
            full_comparison_key: tp.Optional[str] = None,
            summary_key: tp.Optional[str] = None,
    ):
        """Init method.

        Parameters
        ----------
        criteria : TimeseriesRefCriterion, optional
            The criterion to be used to prepare the output data. Can be omitted
            if `target_range` is a `CriterionTargetRange` or subclass instance
            that contains the desired `Criterion` as its `criterion` attribute.
        target_range : CriterionTargetRange or callable, optional
            A `CriterionTargetRange` or subclass instance that will be used to
            prepare the output data, and contains the desired criterion, target
            value and target range, or a callable that produces such an instance
            using the `criteria`, `target`, `range` and `distance_func`
            parameters. If a `CriterionTargetRange` or subclass instance, those
            parameters are all ignored. If a callable, it must take the
            `TimeseriesRefCriterion` instance passed through the `criteria`
            parameter and returns a `CriterionTargetRange` or subclass instance.
            See the docstring of `CriterionTargetRangeOutput` for details.
            Optional. If not given, an instance of the type given by
            `target_range_type` is constructed using the target, range and
            optionally `distance_func` parameters passed through the `target`,
            `range` and `distance_func` parameters. To access other parameters
            of the `CriterionTargetRange` init method, use a partial function of
            `CriterionTargetRange` as the `target_range` parameter, or pass a
            lambda that calls `CriterionTargetRange` with the parameters set to
            the desired values. If `target_range` is not set, the parameters
            `target_range_type`, `target` and `range` must be set. Subclasses
            can define a default for `target_range_type` by setting the class
            attribute `target_range_default_type`.
        target_range_type : type, optional
            The default type to use to construct a `CriterionTargetRange` or
            subclass instance if `target_range` is not set. Must be a subclass
            of `CriterionTargetRange`, or `CriterionTargetRange` itself.
            Optional, by default uses the class attribute
            `target_range_default_type` if set. If that attribute is not set and
            `target_range` is not set, a MissingDefaultTypeError is raised.
        target : float, optional
            If `target_range` is not set, this parameter is mandatory and used
            to construct a `CriterionTargetRange` instance. A ValueError is
            raised if `target_range` is set and `target` is not None.
        range : 2-tuple of floats or RelativeRange
            If `target_range` is not set, this parameter is mandatory and used
            to construct a `CriterionTargetRange` instance. A ValueError is
            raised if `target_range` is set and `range` is not None.
        distance_func : callable, optional
            If `target_range` is not set, this parameter is used to construct
            a `CriterionTargetRange` instance. A ValueError is raised if
            `target_range` is set and `distance_func` is not None. Optional.
            see the `CriterionTargetRange` docstring for the default behavior.
        timeseries_output : callable, optional
            A function that takes the `TimeseriesRefCriterion` instance passed
            through the `criteria` parameter and returns a
            TimeseriesRefFullComparisonOutput instance, which will be used to
            output the full comparision data. Any writer instance that might be
            set in `timeseries_output` will not be used. The writer passed to
            the `writer` parameter of this class will be used instead. If
            `timeseries_output` is not set, an instance of the type given by
            `timeseries_output_type` is constructed. Optional, if
            `timeseries_output` is not set, `timeseries_output_type` must be
            set. Subclasses can define a default for `timeseries_output_type` by
            setting the class attribute `timeseries_output_default_type`.
        timeseries_output_type : type, optional
            The default type to use to construct a
            `TimeseriesRefFullComparisonOutput` instance if `timeseries_output`
            is not set. Must be a subclass of
            `TimeseriesRefFullComparisonOutput`, or
            `TimeseriesRefFullComparisonOutput` itself. Optional, by default
            uses the class attribute `timeseries_output_default_type` if set.
            If that attribute is not set and `timeseries_output` is not set,
            a MissingDefaultTypeError is raised.
        summary_output : callable, optional
            A function that takes the `CriterionTargetRange` instance passed
            through the `target_range` parameter (or constructed using the
            `target`, `range` and `distance_func` parameters) and returns a
            CriterionTargetRangeOutput instance, which will be used to output
            the summary metrics. Any writer instance that might be set in
            `summary_output` will not be used. The writer passed to the `writer`
            parameter of this class will be used instead. If `summary_output` is
            not set, an instance of the type given by `summary_output_type` is
            constructed. Optional, if `summary_output` is not set, the
            `summary_output_type` must be set. Subclasses can define a default
            for `summary_output_type` by setting the class attribute
            `summary_output_default_type`.
        summary_output_type : type, optional
            The default type to use to construct a `CriterionTargetRangeOutput`
            instance if `summary_output` is not set. Must be a subclass of
            `CriterionTargetRangeOutput`, or `CriterionTargetRangeOutput`
            itself. Optional, by default uses the class attribute
            `summary_output_default_type` if set. If that attribute is not set
            and `summary_output` is not set, a MissingDefaultTypeError is
            raised.
        writer : DataFrameMappingWriter, optional
            The writer to be used to write the output data if either
            `timeseries_output` or `summary_output` is not set. Note that if one
            of those is set but not the other, the `writer` parameter must be
            equal to or at least compatible with the writer instance used by the
            one that is set. If either `timeseries_output` or `summary_output`
            is not set, the `writer` parameter is mandatory. If both are set,
            the `writer` parameter is ignored.
        full_comparison_key : str, optional
            The key to use for the full comparison data in the output dict
            returned by the `prepare_output` method. Optional. If not set, the
            default key "Full comparison" is used.
        summary_key : str, optional
            The key to use for the summary metrics in the output dict
            returned by the `prepare_output` method. Optional. If not set, the
            default key "Summary metrics" is used.
        """
        if criteria is not None:
            if isinstance(target_range, CriterionTargetRange):
                raise TypeError(
                    '`target_range` should not be set to a '
                    '`CriterionTargetRange` instance if `criteria` is provided.'
                )
            if target_range_type is None:
                if hasattr(self, 'target_range_default_type'):
                    target_range_type = self.target_range_default_type
            self.target_range: CriterionTargetRangeTypeVar \
                    = self._prepare_target_range(
                target_range=target_range,
                target_range_type=target_range_type,
                criteria=criteria,
                target=target,
                range=range,
                distance_func=distance_func,
            )
        elif not isinstance(target_range, CriterionTargetRange):
            raise TypeError(
                '`target_range` must be a `CriterionTargetRange` instance if '
                '`criteria` is not provided.'
            )
        else:
            if not isinstance(target_range.criterion, TimeseriesRefCriterion):
                raise TypeError(
                    '`target_range.criterion` must be a `TimeSeriesCriterion` '
                    'instance.'
                )
            self.target_range = target_range
            criteria = target_range.criterion
        self.writer = writer if writer is not None else NoWriter()
        super().__init__(
            criteria=not_none(criteria),
            writer=writer if writer is not None else NoWriter(),
            style=style,
        )
        if timeseries_output_type is None:
            if hasattr(self, 'timeseries_output_default_type'):
                timeseries_output_type = self.timeseries_output_default_type
        if summary_output_type is None:
            if hasattr(self, 'summary_output_default_type'):
                summary_output_type = self.summary_output_default_type
        self.timeseries_output: TimeseriesOutputTypeVar = \
            self._prepare_timeseries_output(
                timeseries_output=timeseries_output,
                timeseries_output_type=timeseries_output_type,
                criteria=criteria,
            )
        self.summary_output: SummaryOutputTypeVar = \
            self._prepare_summary_output(
                summary_output=summary_output,
                summary_output_type=summary_output_type,
                target_range=self.target_range,
            )
        self.full_comparison_key: str = \
            full_comparison_key if full_comparison_key is not None \
                else 'Full comparison'
        self.summary_key: str = summary_key if summary_key is not None \
            else 'Summary metrics'
    ###END def TimeseriesComparisonOutput.__init__

    def _prepare_target_range(
            self,
            target_range: Callable[
                [TimeseriesRefCriterionTypeVar],
                CriterionTargetRangeTypeVar
            ] | None,
            target_range_type: tp.Type[CriterionTargetRangeTypeVar] | None,
            criteria: TimeseriesRefCriterionTypeVar,
            target: float | None,
            range: tp.Tuple[float, float] | RelativeRange | None,
            distance_func: tp.Callable[[float], float] | None,
    ) -> CriterionTargetRangeTypeVar:
        """Prepare a CriterionTargetRange or subclass instance for output.

        This method can be overridden by subclasses to customize how
        `target_range` is used to create a `CriterionTargetRange` or subclass
        instance, and/or how a default is created if `target_range` is None.
        """
        if target_range is not None:
            return target_range(criteria)
        else:
            if target_range_type is None:
                raise ValueError(
                    'Either `target_range` or `target_range_type` must be set.'
                )
            return target_range_type(
                criterion=criteria,
                target=target,
                range=range,
                distance_func=distance_func,
            )
    ###END def TimeseriesComparisonOutput._prepare_target_range

    def _prepare_timeseries_output(
            self,
            timeseries_output: Callable[
                [TimeseriesRefCriterionTypeVar],
                TimeseriesOutputTypeVar
            ] | None,
            timeseries_output_type: tp.Type[TimeseriesOutputTypeVar] | None,
            criteria: TimeseriesRefCriterionTypeVar,
    ) -> TimeseriesOutputTypeVar:
        """Prepare a TimeseriesOutput or subclass instance for output.

        This method can be overridden by subclasses to customize how
        `timeseries_output` is used to create a `TimeseriesOutput` or subclass
        instance, and/or how a default is created if `timeseries_output` is
        None.
        """
        if timeseries_output is not None:
            return timeseries_output(criteria)
        else:
            if timeseries_output_type is None:
                raise ValueError(
                    'Either `timeseries_output` or `timeseries_output_type` '
                    'must be set.'
                )
            return timeseries_output_type(
                criteria=criteria,
                writer=NoWriter(),
            )
    ###END def TimeseriesComparisonOutput._prepare_timeseries_output

    def _prepare_summary_output(
            self,
            summary_output: Callable[
                [CriterionTargetRangeTypeVar],
                SummaryOutputTypeVar
            ] | None,
            summary_output_type: tp.Type[SummaryOutputTypeVar] | None,
            target_range: CriterionTargetRangeTypeVar,
    ) -> SummaryOutputTypeVar:
        """Prepare a SummaryOutput or subclass instance for output.

        This method can be overridden by subclasses to customize how
        `summary_output` is used to create a `SummaryOutput` or subclass
        instance, and/or how a default is created if `summary_output` is
        None.
        """
        if summary_output is not None:
            return summary_output(target_range)
        else:
            if summary_output_type is None:
                raise ValueError(
                    'Either `summary_output` or `summary_output_type` '
                    'must be set.'
                )
            return summary_output_type(
                criteria=target_range,
                writer=NoWriter(),
                style=self.style,
            )
    ###END def TimeseriesComparisonOutput._prepare_summary_output

    def prepare_output(
            self,
            data: pyam.IamDataFrame,
            *,
            criteria: tp.Optional[TimeseriesRefCriterionTypeVar] = None,
    ) -> dict[str, pd.DataFrame]:
        """Prepare DataFrames with full comparison and with summary metrics.

        Parameters
        ----------
        data : pyam.IamDataFrame
            The data to be used in the output.
        criteria : TimeseriesRefCriterion or None
            The criteria to be used in the output. Uses `self.criteria` by
            default. Note that using anything else may give unexpected results,
            since the `TimeseriesRefComparisonAndTargetOutput` class contains
            components that have been initialized with `self.criteria`. Only set
            this parameter to something else if you know what you're doing.

        Returns
        -------
        dict
            A dictionary with the following keys:
            * `self._full_comparison_key`: The full comparison DataFrame
            * `self._summary_key`: The summary metrics DataFrame
        """
        # NB! The code below is probably quite inefficient, as the
        # `prepare_output` calls of both `_full_data_output` and
        # `_summary_output` will call `self.criteria.get_values`, which
        # can be expensive. This should be fixed, maybe by enabling
        # `TimeseriesRefCriterion.get_values` to cache its return value.
        full_comparison: pd.DataFrame = \
            self.timeseries_output.prepare_output(data, criteria=criteria)
        summary_metrics: pd.DataFrame = \
            self.summary_output.prepare_output(data, criteria=self.target_range)
        return {
            self.full_comparison_key: full_comparison,
            self.summary_key: summary_metrics,
        }
    ###END def TimeseriesComparisonOutput.prepare_output

    def style_output(
            self,
            output: dict[str, pd.DataFrame]
    ) -> dict[str, PandasStyler]:
        if self.summary_output.style is None:
            warnings.warn(
                'No summary output style has been specified, `style_outpout` '
                'will return a pandas `Styler` with no styles applied.'
            )
            return {_key: _df.style for _key, _df in output.items()}
        if set(output.keys()) != {self.full_comparison_key, self.summary_key}:
            raise ValueError(
                f'`output` has keys {list(output.keys())}, expected '
                f'{[self.full_comparison_key, self.summary_key]}'
            )
        summary_styler: PandasStyler = \
            self.summary_output.style_output(output[self.summary_key])
        full_comparison_styler: PandasStyler = \
            self.summary_output.styling_funcs[CTCol.VALUE](
                output[self.full_comparison_key].style
            )
        full_comparison_styler = self.summary_output.apply_common_styling(
            full_comparison_styler,
        )
        return {
            self.summary_key: summary_styler,
            self.full_comparison_key: full_comparison_styler,
        }
    ###END def TimeseriesComparisonOutput.style_output

    @property
    def summary_columns(self) -> Sequence[CTCol]:
        """The columns included in the summary output, as `CTCol` enums."""
        return self.summary_output._default_columns
    ###END def TimeSeriesRefComparisonAndTargetOutput.summary_columns

    @property
    def summary_column_titles(self) -> Mapping[CTCol, str]:
        """Dict of the titles of the columns included in the summary output."""
        return self.summary_output._default_column_titles
    ###END def TimeSeriesRefComparisonAndTargetOutput.summary_column_titles

    @property
    def target(self) -> float:
        """Target for the values returned by the timeseries criterion."""
        return self.summary_output.criteria.target
    ###END def TimeSeriesRefComparisonAndTargetOutput.target

    @property
    def range(self) -> tuple[float, float]:
        """Target range for the values returned by the timeseries criterion."""
        return self.summary_output.criteria.range
    ###END def TimeSeriesRefComparisonAndTargetOutput.target_range

    @property
    def relative_range(self) -> RelativeRange | None:
        """Relative range for values returned by the timeseries criterion.

        If the range was originally specified in terms of values relative to
        `target` (i.e., as a `RelativeRange` instance), this will return that
        range, equal to `range` with each element divided by `target`. If the
        range was originally specified in terms of absolute values, `None` will
        be returned.
        """
        return self.summary_output.criteria.relative_range
    ###END def TimeSeriesRefComparisonAndTargetOutput.target_range

    def is_in_range(self, value: float) -> bool:
        """Checks whether a single number is in the target range."""
        return self.summary_output.criteria.is_in_range(value)
    ###END def TimeSeriesRefComparisonAndTargetOutput.is_in_range

    def is_below_range(self, value: float) -> bool:
        """Checks whether a single number is below the target range."""
        return self.summary_output.criteria.is_below_range(value)
    ###END def TimeSeriesRefComparisonAndTargetOutput.is_below_range

    def is_above_range(self, value: float) -> bool:
        """Checks whether a single number is above the target range."""
        return self.summary_output.criteria.is_above_range(value)
    ###END def TimeSeriesRefComparisonAndTargetOutput.is_above_range

###END class TimeseriesRefComparisonAndTargetOutput


class TimeseriesRefTargetOutput(
    TimeseriesRefComparisonAndTargetOutput[
        TimeseriesRefCriterion,
        CriterionTargetRange,
        TimeseriesRefFullComparisonOutput,
        CriterionTargetRangeOutput,
        MultiDataFrameExcelWriter | NoWriter,
        None,
        CriterionTargetRangeOutputStyles
    ]
):
    """Less generic, friendlier `TimeseriesRefComparisonAndTargetOutput`.

    This class produces output from a timeseries reference data comparison (done
    using a `TimeseriesRefCriterion` instance), with an optional summary. It
    subclasses and produces the same type of output as
    `TimeseriesRefComparisonAndTargetOutput`, but is less generic and has fewer
    but less bewildering customization options. For initialization, it only
    requires a `CriterionTargetRange` instance, which must have been created
    with a `TimeseriesRefCriterion` instance (containing the timeseries
    reference data) passed to the `criterion` parameter of its `__init__`
    method. It sets fixed choices or sensible defaults for all other options in
    the `TimeseriesRefComparisonAndTargetOutput` class.

    Like `TimeseriesRefComparisonAndTargetOutput`, it returns output as a
    dict of `pandas.DataFrame` (one with the full timeseries comparison and
    one with a summary). The summary can optionally be skipped using the
    `with_summary` parameter to `self.prepare_output`.

    In addition, the class supports writing output directly to Excel with a
    `self.to_excel` method.
    """

    def __init__(
            self,
            criterion_target: CriterionTargetRange,
            *,
            full_comparison_key: tp.Optional[str] = None,
            summary_key: tp.Optional[str] = None,
            summary_columns: tp.Optional[Sequence[CTCol]] = None,
            summary_column_titles: tp.Optional[Mapping[CTCol, str]] = None,
            style: tp.Optional[CriterionTargetRangeOutputStyles] = None,
            writer: tp.Optional[MultiDataFrameExcelWriter|NoWriter] = None,
    ) -> None:
        """
        Parameters
        ----------
        criterion_target : CriterionTargetRange
            A CriterionTargetRange instance that will be used to produce the
            output comparison values. Must have been initialized with a
            `TimeseriesRefCriterion` instance as its `criterion` parameter,
            which must contain the timeseries reference data.
        full_comparison_key : str, optional
            The key to use for the `DataFrame` with the full comparison values
            (output of `comparison_function` for all points in all
            non-aggregated dimensions) in the dict returned by `prepare_output`
            and `prepare_styled_output`. When writing to Excel with
            `MultiDataFrameExcelWriter`, this will also be used as the
            corresponding worksheet name. Optional, defaults to `"Full
            comparison"`.
        summary_key : str, optional
            The key to use for the `DataFrame` with the summary values in the
            dict returned by `prepare_output` and `prepare_styled_output`. When
            writing to Excel with `MultiDataFrameExcelWriter`, this will also
            be used as the corresponding worksheet name. Optional, defaults to
            `"Summary"`.
        summary_columns : Sequence[CTCol], optional
            The columns to use for the summary values in the summary DataFrame
            in the dict returned by `prepare_output` and
            `prepare_styled_output`. Optional, defaults to `[CTCol.INRANGE,
            CTCol.VALUE]`, i.e., a column with in-range/out-of-range boolean
            values, a column with aggregated return values from
            `comparison_function` and a column with the
        summary_column_titles : Mapping[CTCol, str], optional
            The titles to use for the summary columns in the summary DataFrame.
            Optional, defaults to `{CTCol.INRANGE: "In range",
            CTCol.VALUE: "Comparison values"}`.
        """
        # if isinstance(reference, IamCompactHarmonizationRatioCriterion):
        #     criterion: IamCompactHarmonizationRatioCriterion = reference
        # else:
        #     if criterion_name is None:
        #         raise ValueError(
        #             'criterion_name must be given if reference is not an '
        #             'IamCompactHarmonizationRatioCriterion instance'
        #         )
        #     criterion = IamCompactHarmonizationRatioCriterion(
        #         criterion_name=criterion_name,
        #         reference=reference,
        #         comparison_function=comparison_function,
        #         region_agg=region_agg,
        #         time_agg=time_agg,
        #         default_agg_dims=default_agg_dims,
        #         broadcast_dims=broadcast_dims,
        #     )
        if not isinstance(criterion_target.criterion, TimeseriesRefCriterion):
            raise ValueError(
            '`criterion_target` must have been initialized with a '
            '`TimeseriesRefCriterion` instance as its `criterion` parameter. '
            '`criterion_target.criterion` instead is of type '
            f'{type(criterion_target.criterion)}.'
        )
        if summary_key is None:
            summary_key = 'Summary'
        if full_comparison_key is None:
            full_comparison_key = 'Full comparison'
        if writer is None:
            writer = NoWriter()
        if summary_columns is None:
            summary_columns = [CTCol.INRANGE, CTCol.VALUE]
        if summary_column_titles is None:
            summary_column_titles = {
                CTCol.INRANGE: 'In range',
                CTCol.VALUE: 'Comparison values',
            }
        # def _make_summary_output_obj(
        #         _target_range: IamCompactHarmonizationTarget,
        # ) -> CriterionTargetRangeOutput:
        #     return CriterionTargetRangeOutput(
        #         criteria=_target_range,
        #         writer=writer,
        #         columns=summary_columns,
        #         column_titles=summary_column_titles
        #     )
        super().__init__(
            target_range=criterion_target,
            timeseries_output_type=TimeseriesRefFullComparisonOutput,
            # summary_output=_make_summary_output_obj,
            summary_output_type=CriterionTargetRangeOutput,
            full_comparison_key=full_comparison_key,
            summary_key=summary_key,
            style=style,
            writer=writer,
        )
    ###END def IamCompactTimeseriesRefComparisonOutput.__init__

    def to_excel(
            self,
            file: ExcelFileSpec | pd.ExcelWriter | MultiDataFrameExcelWriter,
            *,
            results: dict[str, pd.DataFrame] | dict[str, PandasStyler],
            force_valid_sheet_name: bool = True,
    ) -> None:
        """
        Writes the output to an Excel file.

        Parameters
        ----------
        file : str, Path, BytesIO, pandas.ExcelWriter, or MultiDataFrameExcelWriter
            Path or str specifying the Excel file to write to, or a pre-existing
            `xlsxwriter.Workbook` or `pandas.ExcelWriter` object. Can also write
            to an in-memory `BytesIO` object. If using a `pandas.ExcelWriter`
            object, it must use `xlsxwriter` as its engine. Can also use an
            already instantiated `excel.MultiDataFrameExcelWriter` object. Note
            that if `file` is a `MultiDataFrameExcelWriter` or
            `pandas.ExcelWriter` object, it will not be closed after writing.
            The caller is responsible for closing it, and content will most
            likely not be written to disk before that is done.
        results : dict[str, pd.DataFrame], optional
            The dict returned by `prepare_output` (for unstyled Excel output)
            or `prepare_styled_output` (for styled Excel output).
        force_valid_sheet_name : bool, optional
            Whether to modify the keys of the `data` dict passed to `write` to
            be valid Excel sheet names, using the `make_valid_excel_sheetname`
            function. Optional, defaults to True.
        """
        if isinstance(
                file,
                (pd.ExcelWriter, MultiDataFrameExcelWriter,ExcelWriterBase)
        ):
            close_file: bool = False
        else:
            close_file = True
        if not isinstance(file, MultiDataFrameExcelWriter):
            file = MultiDataFrameExcelWriter(
                file=file,
                force_valid_sheet_name=force_valid_sheet_name,
            )
        super().write_output(results, writer=file)
        if close_file:
            file.close()
    ###END def IamCompactTimeseriesRefComparisonOutput.to_excel

###END class IamCompactTimeseriesRefComparisonOutput
