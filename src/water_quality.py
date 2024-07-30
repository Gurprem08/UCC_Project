

# def calculate_WAWQI(predictions,standard_values, ideal_values, weights):
#     subindices = {}
#     del predictions['EC']
#     del predictions['Temperature']
#     for parameter in predictions:
#         Vi = predictions[parameter]  # Directly use the predicted value
#         Si = standard_values[parameter]
#         Ii = ideal_values[parameter]
#         subindices[parameter] = ((Vi - Ii) / (Si - Ii)) * 100
    

    
#     weighted_subindices = {parameter: subindices[parameter] * weights[parameter] for parameter in subindices}
#     WAWQI = sum(weighted_subindices.values()) / sum(weights.values())
    
#     return WAWQI

def calculate_wqi(predictions, standard_values, ideal_values, weights):
    # Step 1: Calculate the Quality Rating (Qn) for each parameter
    del predictions['EC']
    del predictions['Temperature']
    quality_ratings = {}
    for param, observed_value in predictions.items():
        standard_value = standard_values[param]
        ideal_value = ideal_values[param]
        quality_rating = 100 * ((observed_value - ideal_value) / (standard_value - ideal_value))
        quality_ratings[param] = quality_rating
    
    # Step 2: Calculate the Weighted Value for each parameter
    weighted_values = {}
    for param, quality_rating in quality_ratings.items():
        unit_weight = weights[param]
        weighted_value = unit_weight * quality_rating
        weighted_values[param] = weighted_value
    
    # Step 3: Calculate the Water Quality Index (WQI)
    sum_weighted_values = sum(weighted_values.values())
    sum_unit_weights = sum(weights.values())
    wqi = sum_weighted_values / sum_unit_weights
    
    return wqi


