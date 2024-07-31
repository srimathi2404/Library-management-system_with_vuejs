import pandas as pd
import plotly.express as px
from jinja2 import Template
from models import db, Books, BookAccess
import os
from sqlalchemy import extract

# Function to fetch accessed books for a specific user in a given month
def get_monthly_accessed_books(user_id, year, month):
    result = db.session.query(BookAccess, Books).join(Books).filter(
        BookAccess.book_id == Books.id,
        BookAccess.user_id == user_id,
        extract('year', BookAccess.issue_date) == year,
        extract('month', BookAccess.issue_date) == month
    ).all()
    return result

def generate_monthly_report(user_id, year, month):
    # Fetch accessed books for the user in the given month
    accessed_books = get_monthly_accessed_books(user_id, year, month)
    
    # Process the fetched data for the table
    table_data = [{
        'name': item.Books.name,
        'author': item.Books.author,
        'access_date': item.BookAccess.issue_date
    } for item in accessed_books]
    
    # Create a Pandas DataFrame for Plotly chart
    df = pd.DataFrame({
        'Book Name': [item.Books.name for item in accessed_books],
        'Author': [item.Books.author for item in accessed_books],
        'Quantity': [1 for _ in accessed_books]  # assuming quantity as 1 per access
    })

    # Create a bar chart using Plotly Express
    fig = px.bar(df, x='Book Name', y='Quantity', title='Books Accessed')

    # Update layout for better appearance (optional)
    fig.update_layout(
        xaxis_title='Book Name',
        yaxis_title='Access Count',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        bargap=0.2  # Set gap between bars
    )

    # Save the chart as an image
    image_path = f'chart.png'
    fig.write_image(image_path)

    # Read the HTML template
    with open('monthly_report_template.html', 'r') as file:
        template = Template(file.read())

    # Render HTML with table data and image path
    rendered_html = template.render(books=table_data, image_path=image_path)

    # Save the rendered HTML to a file
    report_file = f'report.html'
    if os.path.exists(report_file):
        os.remove(report_file)

    with open(report_file, 'w') as output:
        output.write(rendered_html)

    return report_file
