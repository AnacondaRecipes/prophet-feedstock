from prophet import Prophet

m = Prophet()
print(f'Using backend: {m.stan_backend.get_type()}')
