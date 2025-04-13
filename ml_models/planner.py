import pandas as pd
import random
import os
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activities.csv")
DEFAULT_ACCOMMODATION_COST_RANGE = (250, 400)
DEFAULT_PLAN_DURATION_DAYS = 3
DEFAULT_NUM_PLANS = 3

def filter_activities(df, region, lifestyle, activity_types=None):
    """
    Filter activities based on region, lifestyle, and optional activity types.

    Args:
        df (DataFrame): The activities DataFrame.
        region (str): The target region.
        lifestyle (str): The lifestyle preference.
        activity_types (list, optional): List of activity types to filter by.

    Returns:
        DataFrame: A filtered DataFrame of activities.
    """
    filtered = df[
        (df['region'].str.lower() == region.lower()) &
        (df['lifestyle'].str.lower() == lifestyle.lower())
    ]
    if activity_types:
        filtered = filtered[filtered['type'].isin(activity_types)]
    return filtered

def generate_plans(budget, region, lifestyle, num_plans=DEFAULT_NUM_PLANS, duration_days=DEFAULT_PLAN_DURATION_DAYS):
    """
    Generate travel plans based on budget, region, and lifestyle.

    Args:
        budget (int): The budget in MAD.
        region (str): The target region for the travel plan.
        lifestyle (str): The lifestyle preference (e.g., 'adventure', 'relaxation').
        num_plans (int): Number of plans to generate.
        duration_days (int): Duration of each plan in days.

    Returns:
        dict: A dictionary containing a list of generated plans.
    """
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        logging.error("Data file not found at %s", DATA_PATH)
        return {"error": "Data file not found."}
    except pd.errors.EmptyDataError:
        logging.error("Data file is empty or corrupted.")
        return {"error": "Data file is empty or corrupted."}

    # Normalize inputs
    lifestyle = lifestyle.replace('-', '_').lower()
    region = region.lower()

    # Debugging information
    logging.info("Available lifestyles: %s", df['lifestyle'].unique())
    logging.info("Available regions: %s", df['region'].unique())

    # Filter activities based on region and lifestyle
    filtered = filter_activities(df, region, lifestyle)
    if filtered.empty:
        logging.warning("No activities found for region '%s' and lifestyle '%s'.", region, lifestyle)
        return {"plans": []}

    # Select accommodation
    accommodation_options = filter_activities(df, region, lifestyle, activity_types=['relaxation', 'food'])
    if not accommodation_options.empty:
        selected_accommodation = accommodation_options.sample(1).iloc[0]
        accommodation = {
            "name": selected_accommodation["activity_name"],
            "type": selected_accommodation["type"].capitalize(),
            "cost": selected_accommodation["cost_mad"],
            "description": selected_accommodation["description"]
        }
    else:
        accommodation = {
            "name": "Local Guesthouse",
            "type": "Riad",
            "cost": random.randint(*DEFAULT_ACCOMMODATION_COST_RANGE),
            "description": f"A comfortable traditional stay in {region.title()}."
        }

    plans = []

    for i in range(num_plans):
        remaining_budget = budget
        used_indices = set()
        flat_activities = []

        for day in range(1, duration_days + 1):
            day_activities = []
            for _ in range(random.randint(1, 2)):
                options = filtered[~filtered.index.isin(used_indices)]
                if options.empty:
                    break

                activity = options.sample(1).iloc[0]
                if remaining_budget - activity["cost_mad"] >= 0:
                    used_indices.add(activity.name)
                    remaining_budget -= activity["cost_mad"]
                    act_obj = {
                        "name": activity["activity_name"],
                        "cost": activity["cost_mad"],
                        "duration": f"{activity['duration_hrs']} hrs",
                        "description": activity["type"],
                        "day": day
                    }
                    day_activities.append(act_obj)
                    flat_activities.append(act_obj)

        total_cost = sum(a["cost"] for a in flat_activities) + accommodation["cost"]

        plan = {
            "id": str(uuid.uuid4()),
            "title": f"{lifestyle.replace('_', ' ').title()} Plan {i+1}",
            "description": f"A custom {lifestyle.replace('_', ' ')} travel experience in {region.title()}",
            "activities": flat_activities,
            "totalCost": total_cost,
            "duration": f"{duration_days} days",
            "accommodation": accommodation
        }

        plans.append(plan)

    return {"plans": plans}