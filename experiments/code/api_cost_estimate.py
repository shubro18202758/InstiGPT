pricing_info = {
    "gpt-3.5-turbo-1106": [0.001, 0.002],
    "gpt-3.5-turbo-instruct": [0.0015, 0.002],
    "gpt-4-1106-preview": [0.01, 0.03],
    "gpt-4-1106-vision-preview": [0.01, 0.03],
    "gpt-4": [0.03, 0.06],
    "gpt-4-32k": [0.06, 0.12],
}


def calculate_complex_llm_costs(
    DAU_weekday,
    DAU_weekend,
    PromptsPerUser,
    InputTokensPerPrompt,
    OutputTokensPerPrompt,
    model_usage_split,
    pricing_info,
):
    """
    Calculate the cost of running a large language model application with more complex assumptions.

    :param DAU_weekday: Daily Active Users on weekdays
    :param DAU_weekend: Daily Active Users on weekends
    :param PromptsPerUser: Number of prompts per user per day
    :param InputTokensPerPrompt: Average number of input tokens per prompt
    :param OutputTokensPerPrompt: Average number of output tokens per prompt
    :param model_usage_split: Dictionary with model names and usage percentages
    :param pricing_info: Dictionary with model names and their input/output token costs
    :return: A tuple containing the cost on a daily (weekday and weekend), monthly, and yearly basis
    """

    total_costs = {"weekday": 0, "weekend": 0}

    for model, usage_percent in model_usage_split.items():
        input_cost, output_cost = pricing_info[model]
        for day_type, DAU in [("weekday", DAU_weekday), ("weekend", DAU_weekend)]:
            total_input_tokens = (
                DAU * PromptsPerUser * InputTokensPerPrompt * usage_percent
            )
            total_output_tokens = (
                DAU * PromptsPerUser * OutputTokensPerPrompt * usage_percent
            )

            daily_cost = (
                total_input_tokens * input_cost + total_output_tokens * output_cost
            ) / 1000
            total_costs[day_type] += daily_cost

    monthly_cost = (total_costs["weekday"] * 5 + total_costs["weekend"] * 2) * 4
    yearly_cost = monthly_cost * 12

    return total_costs["weekday"], total_costs["weekend"], monthly_cost, yearly_cost


DAU_weekday = 1000
DAU_weekend = 100
PromptsPerUser = 20  # This is for one day
InputTokensPerPrompt = 4000
OutputTokensPerPrompt = 1000
model_usage_split = {"gpt-3.5-turbo-1106": 1.0, "gpt-4-1106-preview": 0}

weekday_cost, weekend_cost, monthly_cost, yearly_cost = calculate_complex_llm_costs(
    DAU_weekday,
    DAU_weekend,
    PromptsPerUser,
    InputTokensPerPrompt,
    OutputTokensPerPrompt,
    model_usage_split,
    pricing_info,
)

print(
    f"Weekday cost: {weekday_cost} \nWeekend cost: {weekend_cost} \nMonthly cost: {monthly_cost} \nYearly cost: {yearly_cost}"
)
