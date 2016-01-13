# Plugin that find bad coding and regex to good standart coding
# Author : Esteban Fuentealba <esteban@blackhole.cl>
# Version : 1.1
# Last Edit : 13/01/2016

import sublime_plugin
import re


class ReplacerCommand( sublime_plugin.TextCommand ) :
    def run( self, edit ) :
        selection = self.view.sel()
        for region in selection:
            try:
                value = self.view.substr( region )
                self.view.replace( edit, region, self.op( value ) )
            except ValueError:
                pass

    def is_enabled( self ) :
        return len( self.view.sel()) > 0


class BeautycodeCommand( ReplacerCommand ) :

    def op( self, value ) :
        beauty_map = [
            {
                # Pattern to find [var to [ var
                'pattern' : r"\[(\w+|\"|'|\[)(?!\s+)(?!\])",
                'replacement' : r"[ \1"
            },
            {
                # Pattern to find var] to var ]
                'pattern' : r"(\w+|\"|'|\])\](?!\s+)(?!\[)",
                'replacement' : r"\1 ]"
            },
            {
                # Pattern to find (var to ( var
                'pattern' : r"\((\w+|\"|'|\[)",
                'replacement' : r"( \1"
            },
            {
                # Pattern to find  like function(var) to function(var )
                'pattern' : r"([\w+'\$\]])(?!\(\))(?!\s+)\)",
                'replacement' : r"\1 )"
            },
            {
                # Special case like call = class.function(subfunction()) to match the right case to class.function(subfunction() )
                'pattern' : r"\)\)",
                'replacement' : r") )"
            },
            {
                # This pattern find like ='asd' or =$var and add a space after = $var or = 'asd'
                'pattern'     : r"(?!=\s+)=(?!>)",
                'replacement' : r"= "
            },
            {
                # This pattern find like variable=2 or $myvar=1 and replaces to variable =2 and $myvar =1
                'pattern'     : r"([\)'\w+\]])=",
                'replacement' : r"\1 ="
            },
            {
                # This pattern find like =>'asd' or =>$var and add a space after => $var or => 'asd'
                'pattern'     : r"=>([\(\['\$\w+])",
                'replacement' : r"=> \1"
            },
            {
                # var[x]=>var[y],
                # This patter find like variable=>2 or $myvar=>1 and replaces to variable =>2 and $myvar =>1
                'pattern'     : r"(['\)\w+\]])=>",
                'replacement' : r"\1 =>"
            },
            {
                # this pattern find all like asd  =  dds (negation of a = b) or more spaces and replaces for only 1
                'pattern'      : r"(?!\s=\s)\s+=\s+",
                'replacement' : r" = "
            },
            {
                # This pattern find like "variable":2 replaces to "variable" :2 and $myvar =1
                'pattern'      : r"(\"|\'|\d+|\w+)\:",
                'replacement' : r" \1 :"
            },
            {
                # This pattern find like "variable":2 replaces to "variable" :2 and $myvar =1
                'pattern'      : r"\:(\"|\'|\d+|\w+)",
                'replacement' : r": \1"
            },
            {
                # this pattern find all like ($a,'n',asd,function(),$element) and add a space after the comma
                'pattern'      : r"(?!,\s+),",
                'replacement' : r", "
            }
        ]

        for obj in beauty_map:
            pattern     = obj['pattern']
            replacement = obj['replacement']
            if len( re.findall( pattern, value ) ) > 0:
                value = re.sub( pattern, replacement , value )
        return value
