def check_id(transaction_id, series):
    
    if transaction_id.strip() == "":
            
            return "Введите id"
            
    if transaction_id not in series: 
            
        return "Неправильный id"

    return None
