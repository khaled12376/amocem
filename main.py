import streamlit as st
import pandas as pd

# Food emissions data
food_emissions = {
    'Beef': 27.0,
    'Lamb': 39.0,
    'Cheese': 13.5,
    'Pork': 12.0,
    'Turkey': 10.9,
    'Chicken': 6.9,
    'Tuna': 6.1,
    'Eggs': 4.8,
    'Potatoes': 2.9,
    'Rice': 4.5,
    'Nuts': 0.43,
    'Vegetables': 2.0,
    'Lentils': 0.9,
    'Tofu': 2.0
}


def main():
    st.title("Food CO2 Emissions Calculator")
    st.write("Calculate the CO2 emissions from your food choices")

    # Let user select number of foods to calculate
    num_foods = st.number_input("How many different foods would you like to calculate?",
                                min_value=1, max_value=len(food_emissions), value=3)

    st.write("---")
    total_emissions = 0
    calculations = []

    # Create input fields for each food selection
    for i in range(int(num_foods)):
        st.subheader(f"Food {i + 1}")

        # Food selection dropdown
        food = st.selectbox(f"Select food type",
                            options=list(food_emissions.keys()),
                            key=f"food_{i}")

        # Quantity input
        quantity = st.number_input(f"Enter quantity (kg)",
                                   min_value=0.0,
                                   value=1.0,
                                   step=0.1,
                                   key=f"quantity_{i}")

        # Calculate emissions for this food
        emissions = food_emissions[food] * quantity
        total_emissions += emissions

        calculations.append({
            'Food': food,
            'Quantity (kg)': quantity,
            'Emissions Factor': food_emissions[food],
            'Total Emissions (kg CO2)': emissions
        })

        st.write("---")

    # Display results
    if calculations:
        st.subheader("Results")
        df = pd.DataFrame(calculations)
        st.dataframe(df)

        st.success(f"Total CO2 Emissions: {total_emissions:.2f} kg CO2")

        # Create a bar chart of emissions by food
        st.subheader("Emissions Breakdown")
        st.bar_chart(df.set_index('Food')['Total Emissions (kg CO2)'])


if __name__ == "__main__":
    main()