#def testFail():
#    assert False
    
def testCommandWhichOS():    
    import please2.command_line
    from please2.command.cmd_base import Args
    result = please2.command_line.process(Args('which OS'.split()))
    print(result)
    assert(result.get('OS', '').lower() == 'linux')
