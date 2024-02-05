from soil_api.config import settings
from soil_api.models.soil import (
    DepthRange,
    SoilDepth,
    SoilLayer,
    SoilPropertiesCodes,
    SoilPropertiesNames,
    SoilPropertiesUnits,
    SoilPropertyValues,
)


def generate_soil_layer(
    property: str, soil_map_info: dict[dict[str, int]]
) -> SoilLayer:
    """Generate a soil layer.

    Parameters:
    - property (str): The soil property to generate the layer for.
    - soil_map_info (dict): The soil map information.

    Returns:
    SoilLayer: The generated soil layer.
    """
    depths = list(soil_map_info.keys())
    soil_depths = []
    for depth in depths:
        values = soil_map_info[depth]
        soil_depths.append(generate_soil_depth(values, depth, settings.depths[depth]))

    return SoilLayer(
        code=SoilPropertiesCodes.__members__[property],
        name=SoilPropertiesNames.__members__[property],
        unit=SoilPropertiesUnits.__members__[property],
        depths=soil_depths,
    )


def generate_soil_depth(
    values: dict[str, int], depth: str, depth_range: dict
) -> SoilDepth:
    """Generate a soil depth.

    Parameters:
    - values (dict): The soil property values.
    - depth (str): The soil depth label.
    - depth_range (dict): The soil depth range.

    Returns:
    SoilDepth: The generated soil depth.
    """
    soil_prop_values = SoilPropertyValues(**values)
    depth_range = DepthRange(**depth_range)

    return SoilDepth(
        range=depth_range,
        label=depth,
        values=soil_prop_values,
    )
