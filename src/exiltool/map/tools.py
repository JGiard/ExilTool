def compute_prod(land: int, native_prod: int):
    base_occupation = 9 + 2 + 2 + 6 + 6 + 2  # colony + construction + energy + storage + factories + naval yard
    mines = int((land + 20 - base_occupation) / 2)
    travs = 40000 - 9000 - mines * 1000  # base buildings + 10 sats
    while travs < 0:
        mines -= 1
        travs += 6000
    prod = native_prod + mines * native_prod * 4
    prod_total = prod * ((100 + mines) / 100) * 1.14 * 1.10  # techs + buildings, efficency
    return int(prod_total)
