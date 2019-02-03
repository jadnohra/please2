#def testFail():
#    assert False
    
def testCommandWhichOS():    
    import please2.command_line
    result = please2.command_line.process('which OS')
    print(result)
    assert(result.get('OS', '').lower() == 'linux')
