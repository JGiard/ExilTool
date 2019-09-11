def compute_prod(land: int, native_prod: int):
    mines = int((land - 20) / 2)
    prod = native_prod + mines * native_prod * 4
    prod_eff = prod * 1.10
    prod_total = prod * ((100 + mines) / 100)
    return prod_total
