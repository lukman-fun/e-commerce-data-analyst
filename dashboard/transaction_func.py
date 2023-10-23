class TransactionFunc:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_daily_order_and_revenue_df(self):
        daily_orderd_and_revenue_df = self.df.resample(rule='D', on='order_approved_at').agg({
            'order_id': 'nunique',
            'payment_value': 'sum'
        })

        daily_orderd_and_revenue_df = daily_orderd_and_revenue_df.reset_index()
        daily_orderd_and_revenue_df.rename(columns={
            'order_id': 'order_count',
            'payment_value': 'revenue'
        }, inplace=True)

        return daily_orderd_and_revenue_df
    
    def create_product_best_and_worst_df(self):
        product_best_and_worst_df = self.df.groupby(by='product_category_name_english').product_id.count().sort_values(ascending=False).reset_index()
        product_best_and_worst_df.rename(columns={
            'product_category_name_english': 'category_name',
            'product_id': 'total_quantity'
        }, inplace=True)

        product_best_and_worst_df['category_name'] = product_best_and_worst_df['category_name'].str.replace('_', ' ')

        return product_best_and_worst_df
    
    def create_customer_demographic_bystate_df(self):
        customer_demographic_bystate_df = self.df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False).reset_index()
        customer_demographic_bystate_df.rename(columns={
            'customer_id': 'customer_count'
        }, inplace=True)

        return customer_demographic_bystate_df
    
    def create_customer_demographic_bycity_df(self):
        customer_demographic_bycity_df = self.df.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False).reset_index()
        customer_demographic_bycity_df.rename(columns={
            'customer_id': 'customer_count'
        }, inplace=True)

        return customer_demographic_bycity_df
    
    def create_customer_order_status_df(self):
        customer_order_status_df = self.df.groupby(by='order_status').customer_id.nunique().sort_values(ascending=False).reset_index()
        customer_order_status_df.rename(columns={
            'customer_id': 'customer_count'
        }, inplace=True)

        return customer_order_status_df

    def create_customer_spend_money_df(self):
        customer_spend_money_df = self.df.groupby(by='customer_id').price.sum().sort_values(ascending=False).reset_index()

        return customer_spend_money_df

    def create_review_score_df(self):
        review_score_df = self.df.groupby(by='review_score').customer_id.nunique().sort_values(ascending=False).reset_index()
        review_score_df.rename(columns={
            'customer_id': 'customer_count'
        }, inplace=True)

        return review_score_df