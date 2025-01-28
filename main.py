import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from datetime import datetime

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


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Food CO2 Emissions Report', 0, 1, 'C')
        self.ln(10)


def create_pdf(calculations, total_emissions):
    pdf = PDF()
    pdf.add_page()

    # Date
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.ln(5)

    # Table headers
    pdf.set_font('Arial', 'B', 10)
    col_width = pdf.w / 4.5
    row_height = 10

    headers = ['Food', 'Quantity (kg)', 'Emissions Factor', 'Total (kg CO2)']
    for header in headers:
        pdf.cell(col_width, row_height, str(header), 1)
    pdf.ln()

    # Table rows
    pdf.set_font('Arial', '', 10)
    for calc in calculations:
        pdf.cell(col_width, row_height, str(calc['Food']), 1)
        pdf.cell(col_width, row_height, f"{calc['Quantity (kg)']:.1f}", 1)
        pdf.cell(col_width, row_height, f"{calc['Emissions Factor']:.1f}", 1)
        pdf.cell(col_width, row_height, f"{calc['Total Emissions (kg CO2)']:.1f}", 1)
        pdf.ln()

    # Total
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, row_height, f'Total CO2 Emissions: {total_emissions:.2f} kg CO2', 0, 1)

    return pdf


def get_pdf_download_link(pdf, filename):
    """Generates a link allowing the PDF to be downloaded"""
    # Create the binary stream
    pdf_data = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 Download PDF Report</a>'
    return href


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
        col1, col2 = st.columns(2)

        with col1:
            food = st.selectbox(f"Select food {i + 1}",
                                options=list(food_emissions.keys()),
                                key=f"food_{i}")

        with col2:
            quantity = st.number_input(f"Quantity (kg)",
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

    # Display results
    if calculations:
        st.write("---")
        st.subheader("Results")
        df = pd.DataFrame(calculations)
        st.dataframe(df)

        st.success(f"Total CO2 Emissions: {total_emissions:.2f} kg CO2")

        # Create a bar chart of emissions by food
        st.subheader("Emissions Breakdown")
        chart_data = df.set_index('Food')['Total Emissions (kg CO2)']
        st.bar_chart(chart_data)

        # Create PDF report
        try:
            pdf = create_pdf(calculations, total_emissions)
            st.markdown(get_pdf_download_link(pdf, "food_emissions_report.pdf"), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")


if __name__ == "__main__":
    main()