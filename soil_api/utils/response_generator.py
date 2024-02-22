from soil_api.models.soil_property import (
    DepthRange,
    SoilDepth,
    SoilDepthLabels,
    SoilLayer,
    SoilPropertiesCodes,
    SoilPropertyUnit,
    SoilPropertyValues,
    soil_depth_dict,
    soil_property_dict,
)


def generate_soil_layer(
    property: SoilPropertiesCodes, soil_map_info: dict[SoilDepthLabels, dict[str, int]]
) -> SoilLayer:
    """Generate a soil layer.

    Parameters:
    - property (SoilPropertiesCodes): The soil property to generate the layer for.
    - soil_map_info (dict): The soil map information.

    Returns:
    SoilLayer: The generated soil layer.
    """
    depths = list(soil_map_info.keys())
    soil_depths = []
    for depth in depths:
        values = soil_map_info[depth]
        soil_depths.append(generate_soil_depth(values, depth))

    unit_measure = SoilPropertyUnit(
        conversion_factor=soil_property_dict[property]["conversion_factor"],
        mapped_units=soil_property_dict[property]["mapped_units"],
        target_units=soil_property_dict[property]["target_units"],
        uncertainty_unit="",
    )

    return SoilLayer(
        code=property,
        name=soil_property_dict[property]["name"],
        unit_measure=unit_measure,
        depths=soil_depths,
    )


def generate_soil_depth(
    values: dict[str, int],
    depth: SoilDepthLabels,
) -> SoilDepth:
    """Generate a soil depth.

    Parameters:
    - values (dict): The soil property values.
    - depth (SoilDepthLabels): The soil depth.

    Returns:
    SoilDepth: The generated soil depth.
    """
    soil_prop_values = SoilPropertyValues(**values)
    depth_range = DepthRange(**soil_depth_dict[depth])

    return SoilDepth(
        range=depth_range,
        label=depth.value,
        values=soil_prop_values,
    )
