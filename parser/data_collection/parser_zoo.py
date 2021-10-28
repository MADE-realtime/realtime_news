PARSER_ZOO = {}


def add_to_catalog(name):
    def add_wrapper(parser_to_add):
        PARSER_ZOO[name] = parser_to_add
        return parser_to_add
    return add_wrapper