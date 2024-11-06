"""
通过更好的融合混合数据集，来得到好的识别性能
"""

import typing as t


class Dataset(t.Protocol):
    def get_count(self) -> int: ...
    def limit_size(self, count: int): ...


def comfusion_data(
    percent: int,
    real_data: Dataset,
    generated_data: Dataset,
    merge_data: t.Callable[[Dataset, Dataset], Dataset],
):
    """
    percent: 生成数据所占混合比例
    real_data: 真实数据
    generated_data: 生成数据
    """

    count = real_data.get_count() / (1 - percent)
    generated_data.limit_size(count)

    final_data = merge_data(real_data, generated_data)
    return final_data
