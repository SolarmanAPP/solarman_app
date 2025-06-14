
def estimate_solar_financing(area_kwh_month, home_sqft, cost_per_watt=None,
                              financing_rate=4.5, loan_years=20, tax_credit=0.30):
    """
    Estimates solar system cost and monthly payment based on electricity usage and home size.

    Inputs:
        area_kwh_month (float): user's average monthly electricity usage in kWh
        home_sqft (float): size of the home in square feet
        cost_per_watt (float): installed cost per watt ($/W). If None, uses national average.
        financing_rate (float): annual loan interest rate (in %)
        loan_years (int): loan term duration in years
        tax_credit (float): federal solar Investment Tax Credit (ITC) portion (e.g., 0.30 for 30%)

    Returns:
        dict with keys: system_size_kw, gross_cost, net_cost, monthly_payment
    """

    # Constants / benchmarks
    AVG_USAGE_PER_KW = 855  # average US household monthly kWh
    AVG_COST_PER_WATT = cost_per_watt or 3.00  # $/W range $2.74–$3.30

    # Derive system size needed (kW)
    normalized_usage = area_kwh_month / AVG_USAGE_PER_KW
    system_kw = normalized_usage * 11  # average system ~11 kW

    # Cost calculations
    gross_cost = system_kw * 1000 * AVG_COST_PER_WATT
    net_cost = gross_cost * (1 - tax_credit)

    # Loan amortization monthly payment
    r = financing_rate / 100 / 12
    n = loan_years * 12
    monthly_payment = (net_cost * r) / (1 - (1 + r)**(-n))

    return {
        "system_size_kw": round(system_kw, 2),
        "gross_cost": round(gross_cost, 2),
        "net_cost_after_incentives": round(net_cost, 2),
        "estimated_monthly_payment": round(monthly_payment, 2)
    }
