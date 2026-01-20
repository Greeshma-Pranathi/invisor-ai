# Customer Segmentation – Feature Selection

## Objective
Select meaningful customer attributes for unsupervised segmentation
based on behavior, usage, and profile characteristics.

## Excluded Columns
The following columns were excluded to prevent leakage and noise:
- customer_id (identifier)
- churn (target variable)
- model-related metadata

## Selected Numerical Features
- tenure_months
- monthly_charges
- total_charges
- avg_monthly_usage_gb
- support_tickets_last_6m
- late_payments_last_year

These features represent customer value, usage intensity, and engagement.

## Selected Categorical Features
- senior_citizen
- partner
- dependents
- contract_type
- internet_service
- paperless_billing
- autopay_enabled
- online_security
- tech_support
- streaming_tv
- streaming_movies
- multiple_lines

These features capture customer profile, service adoption, and billing behavior.

## Notes
High-cardinality features such as payment_method and region were deferred
to avoid over-fragmentation in early segmentation iterations.
