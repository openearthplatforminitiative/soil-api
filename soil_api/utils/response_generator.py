from soil_api.models.soil_property import (
    DepthRange,
    SoilDepth,
    SoilDepthBottom,
    SoilDepthLabels,
    SoilDepthTop,
    SoilDepthUnits,
    SoilLayer,
    SoilPropertiesCodes,
    SoilPropertiesNames,
    SoilPropertiesUnits,
    SoilPropertyValues,
    get_soil_depth_from_label,
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
    for depth_label in depths:
        values = soil_map_info[depth_label]
        depth = get_soil_depth_from_label(depth_label)
        soil_depths.append(generate_soil_depth(values, depth))

    return SoilLayer(
        code=SoilPropertiesCodes.__members__[property],
        name=SoilPropertiesNames.__members__[property],
        unit=SoilPropertiesUnits.__members__[property],
        depths=soil_depths,
    )


def generate_soil_depth(
    values: dict[str, int],
    depth: str,
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
    depth_range = DepthRange(
        top_depth=SoilDepthTop.__members__[depth],
        bottom_depth=SoilDepthBottom.__members__[depth],
        unit_depth=SoilDepthUnits.__members__[depth],
    )

    return SoilDepth(
        range=depth_range,
        label=SoilDepthLabels.__members__[depth],
        values=soil_prop_values,
    )
