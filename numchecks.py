
def luhnCheck(n):
    """ 
        luhn check for credit card numbers (and other things).
        Source: https://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#Python
    """
    r = [int(ch) for ch in str(n)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

def luhnCheckAll(str):
    res = []
    if (len(str) < 10): return res;
    for i in range(0, len(str) - 10):
        if (luhnCheck(str[i:])): res.append(str[i:])
        
    return res;