from argpi import PathWays, Definition

definition: Definition
path: PathWays

def test_definition():
    global definition

    definition = Definition([
        {
            'name': 'abc',
            'value': 'abc',
            'short': '-a',
        }
    ])

    definition.add('xyz', 'xyz', '-x')
    definition.add('demo', 'demo', 'demo')
    definition.delete('demo')

    assert definition.count == 2

def test_pathway():
    global definition, path
    def abc(*args, **kwargs):
        return args, kwargs
    
    path = PathWays(definition)

    path.register('abc', abc, 'EXEC', ('hehe', 'hehe2'))
    path.orchestrate

    assert type(path.result_of('abc')) == tuple
    print(path.result_of('abc'))

    assert path.result_of('abc') == (('hehe', 'hehe2'), {})

test_definition()
test_pathway()