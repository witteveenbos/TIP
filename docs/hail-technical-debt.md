## Tech debt

1.  [highkey-fuckaround-findout-debt] An update to developments/maps/graphs do not invalidate the cache for inputs meaning that only manual flush will work
2. [optimisation][CICD] fill the cache every time we release a new version of the app?
3. [refactor][clean-code] A lot of CamelCase and snake_case intertwined
4. [refactor] We have both `ETMScenario` and `MunicipalScenario`, one datamodel should be enough
5. [optimisation] Move `id_to_region_map` function from `util` module to be an attribute on `ContextProvider` (so only compute once per lifetime and store as private `_property`)
6. [optimisation] Don't calculate the developments all the time when `ViewSettings` `AreaDivision.GM` because it should be stored in the frontend (so only on initial call)
7. [refactor] Loads of refactoring and renaming
8.  [tests][refactor] Refactor tests to use a fixture object for Context, not importing (to conftest)
9.  [optimisation] The graph object is using all matrices even when that's not needed
10. [tests] implement tests for graphs and the netload map
11. [optimisation] Refactor the `compute_all_developments` calculation workflow so that all elements are calculated async (now sync, whats better?)
12. [tests] Implement tests for the higher level aggrate functions of map objects 
13. [tests] Implement tests for aggregation (aggregationconfig)
    1. Maps
    2. Developments
14. [refactor] Move the gridload functionality over to the generic aggregate function
15. [refactor] Rename inputs to developments when talking about the sectoral/continuous
16. [tests] Implement tests for `user_original` implementation at the `MultiScenarioData` object
    1. Is the order guaranteed?
    2. Are the values inserted at the right point?
17. [optimisation] Implement np.Nan over None in Matrix because it might implement the same logic as we have now custom
18. [documentation] Complicated tests and functions should have doc strings 
19. [refactor] Tests could be refactored
20. [tests] Add end-to-end tests
21. [documentation] Write documentation
