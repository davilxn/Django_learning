import math

def make_pagination_range(
    page_range_f, 
    qty_pages,
    current_page
):
    middle_range = math.ceil(qty_pages / 2)     
    stop_range = current_page + middle_range    
    start_range = current_page - middle_range   
    total_pages = len(page_range_f)             
    
    """ 
        # middle_range: O índice que fica no meio do range que será mostrado
        # stop_range: Onde o range que será mostrado termina. Note que qty_pages = current_page + middle_range
        # start_range: Onde o range que será mostrado começa.
        # page_range_f é um range da quantidade total de páginas, nesse caso, (1, 113), obtido com o atributo .page_range da classe Paginator. 
        Também podemos, na view home, usar o atributo: .num_pages, mas retornar um range é mais simples, pois usaremos em um for.
    """

    if start_range < 0:
        start_range_offset = abs(start_range)       # Se o valor do start_range for negativo (Se a current_page for 0, por exemplo), essa variável recebe o valor, só que positivo.
    else:
        start_range_offset = 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        stop_range = total_pages
        start_range = start_range - abs(total_pages - stop_range) # Faz todo sentido.

    
    pagination_f = page_range_f[start_range:stop_range]
    return {
        'pagination_ff': pagination_f,          # Range de índices que vai ser mostrado, modificando, a cada chamada, o start_range e o stop_range.
        'page_range': page_range_f,             # Total de índices existentes (112, pois tem 112 páginas)
        'qty_pages': qty_pages,                 # Quantidade de índices a ser mostrada. Valor fixo.
        'current_page': current_page,           # Página atual
        'total_pages': total_pages,             # Quantidade total de páginas
        'star_range': start_range,              # Onde o range de índices vai começar - Valor modificado a cada chamada da função
        'stop_range': stop_range,               # Onde o range de índices vai terminar - Valor modificado a cada chamada da função
        'first_page_out_of_range': current_page > middle_range,     # Se o índice 1 pode ser visto dentro do range.
        'last_page_out_of_range': stop_range < total_pages,         # Se o índice 112 pode ser visto dentro do range.
    }

