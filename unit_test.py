#def testFail():
#    assert False
    
def testCommandWhichOS():    
    import please2.command_line
    print(please2.command_line.process('which OS'))
