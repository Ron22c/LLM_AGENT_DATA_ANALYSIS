import pandas as pd
import numpy
import agent

def sales_data_prediction():
    numpy.random.seed(42)

    dates = pd.date_range(start='2025-01-01', end='2025-01-31', freq='D')

    df = pd.DataFrame({
        'date': dates,
        'category': numpy.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], size=len(dates)),
        'store_id': numpy.random.choice(['Store_'+str(i) for i in range(1,6)], size=len(dates)),
        'sales': numpy.random.normal(1000, 200, size=len(dates)),
        'temparature': numpy.random.normal(20, 5, size=len(dates)),
        'weekend': dates.dayofweek >= 5
    })

    df['sales'] = df['sales'] * (1.2 * df['weekend'])
    df.loc[df['category'] == 'Electronics', 'sales'] *= 1.5
    df['sales'] = df['sales'].abs().round(2)

    question = "Analyze sales patterns: calculate total sales by category and show if weekends have higher avarage sales"
    context = """
    Dataframe df has columns:
    - date: daily dates of 2025
    - category: product category ('Electronics', 'Clothing', 'Food', 'Books')
    - store_id: store identifiers
    - sales: daily sales amount
    - temparature: daily temparature
    - weekend: boolean, True for weekends
    """

    solution, result = agent(question=question, data={'df':df}, data_context=context)
    print(solution, result)

if __name__ == "__main__":
    sales_data_prediction()