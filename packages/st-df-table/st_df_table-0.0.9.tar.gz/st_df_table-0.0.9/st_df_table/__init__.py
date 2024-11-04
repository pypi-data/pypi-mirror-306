"""
    .. include:: ../README.md
    .. include:: ../CHANGELOG.md
"""

import os

import pandas as pd
import streamlit.components.v1 as components

_RELEASE = True

if os.getenv("_ST_TABLE_NOT_RELEASE_"):
    _RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_table",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_table", path=build_dir)


def st_table(
    df: pd.DataFrame,
    head_align: str = "center",
    data_align: str = "left",
    head_bg_color: str = "white",
    data_bg_color: str = "white",
    head_color: str = "black",
    data_color: str = "black",
    head_font_weight: str = "bold",
    data_font_weight: str = "normal",
    bordered: bool = True,
    border_color: str = "black",
    border_width: int = 1,
    table_width: int = None,
    sortable: bool = True,
    font: str = "Arial",
    font_size: int = 16,
    paginated: bool = False,
    pagination_size_per_page: int = 10,
    pagination_bar_size: int = 5,
    pagination_bar_height: int = 14,
    pagination_text_color: str = "black",
    pagination_bg_color: str = "white",
    pagination_border_color: str = "black",
    pagination_active_color: str = "white",
    pagination_active_border_color: str = "black",
    pagination_active_bg_color: str = "gray",
    pagination_hover_color: str = "white",
    pagination_hover_bg_color: str = "gray",
    pagination_show_total: bool = False,
    vertical_alignment: str = "middle",
    key=None,
):
    """Displays Pandas DataFrame

    :param df: pd.DataFrame
    :param head_align: str - aligning table header, values are: "center", "left", "right"
    :param data_align: str - align table data, values are: "center", "left", "right"
    :param head_bg_color: str - table header background color
    :param data_bg_color: str - table data background color
    :param head_color: str - table header text color
    :param data_color: str - table data text color
    :param head_font_weight: str - table header font weight
    :param data_font_weight: str - table data font weight
    :param bordered: bool - table bordered
    :param border_color: str - table border color
    :param border_width: int - table border width in pixels
    :param table_width: int - table width in pixels
    :param sortable: bool - table columns sortable
    :param font: str - table font name
    :param font_size: int - table font size in pixels
    :param paginated: bool - table paginated - **if this is False all below pagination parameters are disregarded**
    :param pagination_size_per_page: int - number of records per page
    :param pagination_bar_size: int - pagination bar size - number of paged displayed on pagination bar
    :param pagination_bar_height: int - pagination bar height
    :param pagination_text_color: str - text color of pagination bar
    :param pagination_bg_color: str - background color of pagination bar
    :param pagination_border_color: str - border color of pagination bar
    :param pagination_active_color: str - active text color of pagination bar
    :param pagination_active_border_color: str - active border color of pagination bar
    :param pagination_active_bg_color: str - active background color of pagination bar
    :param pagination_hover_color: str - hover text color of pagination bar
    :param pagination_hover_bg_color: str - hover background color of pagination bar
    :param pagination_show_total: bool - whether to show total info
    :param vertical_alignment: str - vertical alignment of table rows,
        allowed values are:
            top - Aligns content to the top of the cell.
            middle - Centers content vertically within the cell.
            bottom - Aligns content to the bottom of the cell.
    :param key: str
            An optional key that uniquely identifies this component. If this is
            None, and the component's arguments are changed, the component will
            be re-mounted in the Streamlit frontend and lose its current state.

    :return: none

    """
    columns = [{"dataField": col, "text": col, "sort": sortable} for col in df.columns]
    data = df.reset_index().to_dict(orient="records")
    _component_func(
        columns=columns,
        data=data,
        head_align=head_align,
        data_align=data_align,
        head_bg_color=head_bg_color,
        data_bg_color=data_bg_color,
        head_color=head_color,
        data_color=data_color,
        head_font_weight=head_font_weight,
        data_font_weight=data_font_weight,
        bordered=bordered,
        border_color=border_color,
        border_width=border_width,
        table_width=table_width,
        sortable=sortable,
        font=font,
        font_size=font_size,
        paginated=paginated,
        pagination_size_per_page=pagination_size_per_page,
        pagination_bar_size=pagination_bar_size,
        pagination_bar_height=pagination_bar_height,
        pagination_text_color=pagination_text_color,
        pagination_bg_color=pagination_bg_color,
        pagination_border_color=pagination_border_color,
        pagination_active_color=pagination_active_color,
        pagination_active_border_color=pagination_active_border_color,
        pagination_active_bg_color=pagination_active_bg_color,
        pagination_hover_color=pagination_hover_color,
        pagination_hover_bg_color=pagination_hover_bg_color,
        pagination_show_total=pagination_show_total,
        vertical_alignment=vertical_alignment,
        key=key,
    )
