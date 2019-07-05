import json

class FileIO:

    _instance = None	
    @staticmethod 	
    def getInstance():	
        if FileIO._instance is None:	
            FileIO()	
        return FileIO._instance

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def __init__(self):
        if FileIO._instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.result = []
            FileIO._instance = self

    def reset(self):
        _instance = None

    def __iter__(self):
        return iter(self.result)

    def add_cmd(self, cmd):
        new_cmd = Command(cmd)
        self.result.append(new_cmd)
        return new_cmd

    def get_cmd(self, cmd):
        for i in self.result: 
            if(cmd == i.get_id()):
                return i
        return None

    def add_input(self, cmd, file, hash):
        c = self.get_cmd(cmd)
        if(c == None):
            c = self.add_cmd(cmd)
        c.add_input(file, hash)

    def add_output(self, cmd, file, hash):
        c = self.get_cmd(cmd)
        if(c == None):
            c = self.add_cmd(cmd)
        c.add_output(file, hash)

class Command:
    def __init__(self, id):
        self.cmd = id
        self.input = []
        self.output = []

    def add_input(self, file_name, hash):
        new_file = File(file_name, hash)
        self.input.append(new_file)
        return new_file

    def add_output(self, file_name, hash):
        new_file = File(file_name, hash)
        self.output.append(new_file)
        return new_file
 
    def get_id(self):
        return self.cmd

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

class File:
    def __init__(self, name, hash):
        self.name = name
        self.hash = hash

    def get_name(self):
        return self.name

    def get_hash(self):
        return self.hash

if __name__ == '__main__':

    io = FileIO.getInstance()

    io.add_cmd('cmd1')

    io.add_input('cmd1', 'file1', 'hash1')
    io.add_output('cmd1', 'file2', 'hash2')
    io.add_output('cmd1', 'file3', 'hash3')

    io.add_input('cmd2', 'file4', 'hash4')
    io.add_output('cmd2', 'file5', 'hash5')
    io.add_output('cmd2', 'file6', 'hash6')

    print(io.toJSON())