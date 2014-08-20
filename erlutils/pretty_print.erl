-module(pretty_print).
-export([pretty_print/1]).

pretty_print(BadStr) ->
    {ScanStatus, Scanned_badly_formatted, ScanCount} = erl_scan:string(BadStr),
    {ParseStatus, Parsed_Badly_Formatted} = erl_parse:parse_form(Scanned_badly_formatted),
    erl_pp: form(Parsed_Badly_Formatted).
