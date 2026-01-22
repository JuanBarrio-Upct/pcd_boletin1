import pytest 
def capital_case(x):  
    return x.capitalize()  
def test_capital_case():  
    assert capital_case('semáforo') == 'Semáforo'

def test_raises_exception_on_non_string_arguments():   
    with pytest.raises(TypeError):  
        capital_case(9)

def capital_case(x):  
    if not isinstance(x, str):  
        raise TypeError('Debes de proporcionar un string')         
    return x.capitalize() 