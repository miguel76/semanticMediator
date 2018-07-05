#!/usr/bin/python3

# system-wide requirements
import yaml

class MediatorConfigManagerException(Exception):
    pass    

class ConfigManager:

    mappings = {}
    tools = {"sepa": {}, "sparql-generate": {}}
    
    def __init__(self, configFile):

        # open the configuration file
        try:
            self.config = yaml.load(open(configFile, "r"))
        except FileNotFoundError:
            raise MediatorConfigManagerException("File not found!")

        # read SEPA URIs
        try:
            self.tools["sepa"]["query"] = self.config["sepa"]["URIs"]["query"] 
            self.tools["sepa"]["update"] = self.config["sepa"]["URIs"]["update"]
            self.tools["sepa"]["subscribe"] = self.config["sepa"]["URIs"]["subscribe"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong SEPA Configuration!")

        # read SEPA URIs
        try:
            self.tools["sparqlgen"] = self.config["sparql-generate"]["URI"]
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Wrong SPARQL-generate Configuration!")

        
        # read the mappings
        try:
            
            # iterate over entities (e.g. tracks, collections..)
            for entity in self.config["contentProviders"]["mappings"]:
                
                # iterate over actions (e.g. search..)
                for action in self.config["contentProviders"]["mappings"][entity]:
                    
                    # iterate over content providers (e.g. jamendo, freesound..)
                    for cp in self.config["contentProviders"]["mappings"][entity][action]:

                        # open the file and store the query in memory
                        try:                            
                            fn = self.config["contentProviders"]["mappings"][entity][action][cp]["file"]
                            with open(fn) as fd:

                                # check if dictionary already contains the needed keys
                                if not entity in self.mappings:
                                    self.mappings[entity] = {}
                                if not action in self.mappings[entity]:
                                    self.mappings[entity][action] = {}

                                # read the mapping                                
                                q = fd.read()

                                # if a key is given, put it into the mapping!
                                if cp in self.config["contentProviders"]["keys"]:
                                    q = q.replace("$token", self.config["contentProviders"]["keys"][cp])

                                # store the mapping
                                self.mappings[entity][action][cp] = q
                                
                        except FileNotFoundError:
                            raise MediatorConfigManagerException("Mapping file %s not found!" % fn)
                        
        except (KeyError, TypeError):
            raise MediatorConfigManagerException("Error while reading engine URIs in configuration file!")

    
