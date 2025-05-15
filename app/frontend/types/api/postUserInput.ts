export interface PostUserInputRequest {
    viewSettings: ViewSettings;
    userSettings?: UserSettings | null;
  }
  
  interface ViewSettings {
    areaDivision: "PROV" | "REG" | "GM" | "RES";
    energyCarrier: "all" | "electricity" | "gas" | "heat";
    balance: "balance" | "demand" | "supply";
    original: boolean;
    developmentType: "sectoral" | "continuous";
    mapType: "energy_balance";
    graphType: "energy_balance_bar_chart" | null;
  }
  
  interface UserSettings {
    municipalityScenarios: MunicipalityScenario[];
    continuousDevelopments?: ContinuousDevelopment[] | null;
    sectoralDevelopments?: SectoralDevelopment[] | null;
  }
  
  interface MunicipalityScenario {
    ETMscenarioID: number;
    municipalityID: 
      | "GM0482" | "GM0484" | "GM0489" | "GM0501" | "GM0502" | "GM0503" | "GM0505"
      | "GM0512" | "GM0513" | "GM0518" | "GM0523" | "GM0530" | "GM0531" | "GM0534"
      | "GM0537" | "GM0542" | "GM0546" | "GM0547" | "GM0553" | "GM0556" | "GM0569"
      | "GM0575" | "GM0579" | "GM0590" | "GM0597" | "GM0599" | "GM0603" | "GM0606"
      | "GM0610" | "GM0613" | "GM0614" | "GM0622" | "GM0626" | "GM0627" | "GM0629"
      | "GM0637" | "GM0638" | "GM0642" | "GM1525" | "GM1621" | "GM1783" | "GM1842"
      | "GM1884" | "GM1892" | "GM1901" | "GM1916" | "GM1924" | "GM1926" | "GM1930"
      | "GM1931" | "GM1963" | "GM1978";
  }
  
  interface ContinuousDevelopment {
    municipalityID: 
      | "GM0482" | "GM0484" | "GM0489" | "GM0501" | "GM0502" | "GM0503" | "GM0505"
      | "GM0512" | "GM0513" | "GM0518" | "GM0523" | "GM0530" | "GM0531" | "GM0534"
      | "GM0537" | "GM0542" | "GM0546" | "GM0547" | "GM0553" | "GM0556" | "GM0569"
      | "GM0575" | "GM0579" | "GM0590" | "GM0597" | "GM0599" | "GM0603" | "GM0606"
      | "GM0610" | "GM0613" | "GM0614" | "GM0622" | "GM0626" | "GM0627" | "GM0629"
      | "GM0637" | "GM0638" | "GM0642" | "GM1525" | "GM1621" | "GM1783" | "GM1842"
      | "GM1884" | "GM1892" | "GM1901" | "GM1916" | "GM1924" | "GM1926" | "GM1930"
      | "GM1931" | "GM1963" | "GM1978";
    devGroupKey: string;
    changes: Change[];
  }
  
  interface SectoralDevelopment {
    municipalityID: 
      | "GM0482" | "GM0484" | "GM0489" | "GM0501" | "GM0502" | "GM0503" | "GM0505"
      | "GM0512" | "GM0513" | "GM0518" | "GM0523" | "GM0530" | "GM0531" | "GM0534"
      | "GM0537" | "GM0542" | "GM0546" | "GM0547" | "GM0553" | "GM0556" | "GM0569"
      | "GM0575" | "GM0579" | "GM0590" | "GM0597" | "GM0599" | "GM0603" | "GM0606"
      | "GM0610" | "GM0613" | "GM0614" | "GM0622" | "GM0626" | "GM0627" | "GM0629"
      | "GM0637" | "GM0638" | "GM0642" | "GM1525" | "GM1621" | "GM1783" | "GM1842"
      | "GM1884" | "GM1892" | "GM1901" | "GM1916" | "GM1924" | "GM1926" | "GM1930"
      | "GM1931" | "GM1963" | "GM1978";
    devGroupKey: string;
    changes: Change[];
  }
  
  interface Change {
    devKey: string;
    value: number | null;
  }