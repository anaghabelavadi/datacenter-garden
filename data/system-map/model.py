"""Data center system model: impacts (from the team's taxonomy sheet), drivers,
physical components, signed causal links, stocks & flows, and feedback loops.
Run: python3 model.py <taxonomy.tsv>  -> writes model.json + CSVs, validates."""
import csv, json, re, sys, collections

SRC = sys.argv[1]
rows = list(csv.reader(open(SRC), delimiter="\t"))
h1, h2, h3, h4 = rows[:4]

RENAME = {
    (7, "Gas"): "Gas generation", (8, "Coal"): "Coal generation",
    (27, "Operational"): "Operational CO2", (28, "Embodied in hardware and buildings"): "Embodied CO2",
    (30, "State and national"): "State and national climate targets",
    (31, "Corporate"): "Corporate climate targets",
    (47, "Metals"): "Metals in discharge water",
}

# how the impact can be known (legend in the sheet): M measured/counted, E modelled/estimated,
# Q qualitative/experienced, R relational/contested
KNOW = dict(M="Measured or counted", E="Modelled, estimated or anticipated",
            Q="Qualitative or experienced", R="Relational or contested")
K = {}
for code, labels in {
 "M": """Electricity consumed|Peak load|Speed of load swings|Gas generation|Coal generation|Renewable generation and storage|Clean firm generation (nuclear, geothermal)|Generation outside the public grid|Transmission capacity|Substation and distribution capacity|Availability of grid equipment|Frequency and voltage stability|Wholesale energy price|Capacity price|Household electricity bills|Utility financial health|Natural gas demand|Diesel stored and burned|State and national climate targets|Nitrogen oxides|Fine particulate matter|Sulfur dioxide|Carbon monoxide|Air temperature around sites|Municipal supply drawn|Groundwater level|River and stream flow|Reclaimed water in use|Peak-day water demand|Salinity and dissolved solids|Treatment chemicals and biocides|Metals in discharge water|Water temperature|Sediment and runoff|Fuel and oil contamination|Utility supply capacity|Wastewater plant load|Water price|Farmland|Forest and green space|Wetlands and streams|Impervious surface|Reused industrial land|Land held for power lines and plants|Public access to open space|Hazardous waste|Contamination at disposal sites|Continuous sound level|Low-frequency sound|Intermittent sound|Night-time light|Road traffic|Duration of construction|Construction employment|Operations employment|Availability of skilled trades|Local tax revenue|State tax revenue forgone|Public service and infrastructure spending|Fiscal dependence on one industry|Capital investment|Property values|Connectivity|Debt and financial exposure|Conflict and organised opposition|Public opinion|Public availability of project information|Public availability of contract terms|Public data on energy and water use|National compute capacity|Supplier concentration|Openness of trade in minerals and equipment""",
 "E": """Certainty of future load|Connection headroom for other users|Reserve margin|Flexibility available to grid operators|Stranded-cost exposure|Operational CO2|Embodied CO2|Methane|Water lost to evaporation|Water embedded in electricity|Water embedded in hardware|Habitat extent and connectivity|Birds and wildlife|Groundwater recharge|Copper and aluminium|Gallium|Rare earths|Battery minerals|Semiconductors and memory|Electronic waste|Hardware kept in use|Waste traded across borders|Respiratory illness|Premature death|Cost of health damage|Fire risk|Exposure to hazardous materials|Supply-chain employment|Regional output and income|Investment share of growth|Productivity|Value kept by host regions and countries|Regional self-sufficiency in power|Exposure to supply shocks|Physical attack on facilities|Cyberattack on energy systems|Resilience to extreme heat|Energy saved in other sectors|Energy demand induced elsewhere|Reinvestment of efficiency gains in more computing""",
 "Q": """Archaeological sites|Cemeteries|Historic landscapes and viewsheds|Visual character|Sleep|Stress and anxiety|Emergency vehicle access|Job quality and local share of jobs|Use of home and outdoor space|Daily routines|Rural or residential character|Regional identity|Hope for jobs and renewal|Fear for the community's future|Trust in developers and officials|Visibility of infrastructure and its labour""",
 "R": """Share of grid costs carried by other customers|Corporate climate targets|Allocation among water users|Security of land tenure|Mining pressure on land and communities|Distribution of exposure across places and groups|Room for other businesses to grow|Relation to earlier industrial and extractive history|Sense that promises are kept|Local control over land use|Community say in decisions|Bargaining power relative to developers|Clarity about who has authority|Fit between official metrics and lived experience|Quality of information in public debate|Match between who benefits and who bears costs|Attention to cumulative and regional effects""",
}.items():
    for l in labels.split("|"):
        K[l.strip()] = code

# system-dynamics role of impact variables (default: auxiliary)
STOCKS = set("""Groundwater level|Hardware kept in use|Trust in developers and officials|Conflict and organised opposition|Availability of skilled trades|Farmland|Forest and green space|Wetlands and streams|Impervious surface|Reused industrial land|Land held for power lines and plants|Habitat extent and connectivity|Transmission capacity|Substation and distribution capacity|Debt and financial exposure|National compute capacity|Renewable generation and storage|Clean firm generation (nuclear, geothermal)|Generation outside the public grid|Contamination at disposal sites""".split("|"))
FLOWS = set("""Electricity consumed|Operational CO2|Embodied CO2|Methane|Municipal supply drawn|Water lost to evaporation|Reclaimed water in use|Electronic waste|Hazardous waste|Waste traded across borders|Copper and aluminium|Gallium|Rare earths|Battery minerals|Semiconductors and memory|Local tax revenue|State tax revenue forgone|Capital investment|Natural gas demand|Diesel stored and burned|Groundwater recharge|Nitrogen oxides|Fine particulate matter|Sulfur dioxide|Carbon monoxide|Public service and infrastructure spending""".split("|"))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:48]

nodes = collections.OrderedDict()
def add(label, **kw):
    nid = slug(label)
    assert nid not in nodes, ("dup", label)
    nodes[nid] = dict(id=nid, label=label, **kw)

c1 = c2 = c3 = ""
for j in range(3, len(h4)):
    if h1[j]: c1 = h1[j]
    if h2[j]: c2 = h2[j]
    if h3[j]: c3 = h3[j]
    lab = RENAME.get((j, h4[j]), h4[j])
    if not lab: continue
    assert lab in K, ("no knowability", lab)
    add(lab, group="impact", domain=c1, sub=c2, parent=c3 if c3 != h4[j] else "",
        know=K[lab], role="stock" if lab in STOCKS else "flow" if lab in FLOWS else "aux", col=j)
N_IMPACTS = len(nodes)

# ---- drivers & decision variables (things that act on / are acted on by data centers)
DRIVERS = [
 # domain, label, role, note
 ("Demand and technology", "AI capability", "aux", "What frontier and deployed models can do"),
 ("Demand and technology", "AI adoption and usage", "aux", "Users, queries, enterprise integration"),
 ("Demand and technology", "Demand for compute", "aux", "Training + inference + cloud workloads"),
 ("Demand and technology", "AI and cloud revenue", "flow", "Money returned by compute services"),
 ("Demand and technology", "Chip energy efficiency", "aux", "Compute per watt of new hardware (exogenous trend)"),
 ("Demand and technology", "Model and software efficiency", "aux", "Algorithmic gains, quantisation, distillation"),
 ("Demand and technology", "Cost per unit of compute", "aux", "All-in $ per useful FLOP"),
 ("Demand and technology", "Chip and equipment supply", "aux", "Fab, packaging, HBM and grid-equipment throughput"),
 ("Demand and technology", "Critical mineral prices", "aux", "Ga, REE, Cu, Li price signal"),
 ("Data center decisions", "Investor expectations", "stock", "Accumulated belief in future AI returns"),
 ("Data center decisions", "Data center capex", "flow", "Hyperscaler, neocloud and developer spending"),
 ("Data center decisions", "Planned pipeline", "stock", "Announced / permitted MW not yet under construction"),
 ("Data center decisions", "Capacity under construction", "stock", "MW being built"),
 ("Data center decisions", "Installed IT capacity", "stock", "Operating MW of IT load"),
 ("Data center decisions", "Hardware purchases", "flow", "Servers, GPUs, storage, network bought per year"),
 ("Data center decisions", "Hardware retirement", "flow", "Servers leaving service per year"),
 ("Data center decisions", "Server refresh rate", "aux", "1 / average service life"),
 ("Data center decisions", "Server utilization", "aux", "Share of capacity doing useful work"),
 ("Data center decisions", "Rack power density", "aux", "kW per rack"),
 ("Data center decisions", "PUE", "aux", "Facility energy / IT energy"),
 ("Data center decisions", "Evaporative cooling share", "aux", "Share of heat rejected by evaporating water"),
 ("Data center decisions", "Liquid cooling share", "aux", "Direct-to-chip / immersion share"),
 ("Data center decisions", "Heat reuse", "aux", "Waste heat exported to district heating, greenhouses"),
 ("Data center decisions", "Demand response by data centers", "aux", "Willingness to curtail / shift load"),
 ("Data center decisions", "Clean energy procurement", "aux", "PPAs, 24/7 CFE deals, nuclear restarts"),
 ("Data center decisions", "Developer secrecy", "aux", "NDAs, shell-company names, withheld data"),
 ("Data center decisions", "Community benefit agreements", "aux", "Binding commitments to host communities"),
 ("Data center decisions", "Material recovery from retired hardware", "flow", "Reuse, refurbishment, metal recovery"),
 ("Data center decisions", "Secondary material supply", "stock", "Recovered Cu, Au, Ga, REE available to re-enter use"),
 ("Siting and grid access", "Siting attractiveness", "aux", "Composite pull of a location"),
 ("Siting and grid access", "Power availability at site", "aux", "MW obtainable on a useful timeline"),
 ("Siting and grid access", "Interconnection queue", "stock", "Large-load requests waiting for study / connection"),
 ("Siting and grid access", "Grid connection wait time", "aux", "Years from request to energisation"),
 ("Siting and grid access", "Land availability", "aux", "Suitable, zoned, affordable parcels"),
 ("Siting and grid access", "Permitting speed", "aux", "Speed of local/state approvals"),
 ("Siting and grid access", "Utility grid investment", "flow", "Utility spending on wires, substations, plants"),
 ("Siting and grid access", "Utility rate base", "stock", "Undepreciated utility assets earning a return"),
 ("Policy and governance", "Data center tax incentives", "aux", "Sales/use-tax exemptions, abatements"),
 ("Policy and governance", "Zoning limits and moratoria", "aux", "Local restrictions on where / whether DCs build"),
 ("Policy and governance", "Large-load tariffs", "aux", "Rules making big loads pay for their grid costs, min. take, collateral"),
 ("Policy and governance", "Disclosure rules", "aux", "Mandatory reporting of energy, water, contracts"),
 ("Policy and governance", "Clean energy standards", "aux", "RPS / CES, coal retirement policy"),
 ("External conditions", "Cost of capital", "aux", "Interest rates + risk premium"),
 ("External conditions", "Atmospheric greenhouse gas stock", "stock", "Accumulated CO2e"),
 ("External conditions", "Climate change", "aux", "Warming, heat waves, shifting rainfall"),
 ("External conditions", "Drought and water scarcity", "aux", "Local water stress"),
]
for d, lab, role, note in DRIVERS:
    add(lab, group="driver", domain=d, sub="", know="", role=role, note=note)

# ---- signed causal links:  src > dst : sign : note   (D = notable delay)
LINKS = r"""
AI capability > AI adoption and usage : + : better models find more uses
AI adoption and usage > Demand for compute : + : inference load grows with use
AI adoption and usage > AI and cloud revenue : + :
AI and cloud revenue > Investor expectations : + : revenue validates the narrative
Investor expectations > Data center capex : + :
Cost of capital > Data center capex : - :
Data center capex > Planned pipeline : + :
Data center capex > Capital investment : + :
Data center capex > Debt and financial exposure : + : bond, private-credit and lease financing
Debt and financial exposure > Cost of capital : + : leverage raises risk premium
Demand for compute > Planned pipeline : + :
Siting attractiveness > Planned pipeline : + : where projects get proposed
Planned pipeline > Capacity under construction : + D : construction starts
Permitting speed > Capacity under construction : + :
Capacity under construction > Installed IT capacity : + D : commissioning (duration is an open question)
Installed IT capacity > National compute capacity : + :
National compute capacity > AI capability : + D : more training compute
Installed IT capacity > Cost per unit of compute : - : scale economies
Chip energy efficiency > Cost per unit of compute : - :
Model and software efficiency > Cost per unit of compute : - :
Server utilization > Cost per unit of compute : - :
Chip and equipment supply > Cost per unit of compute : - : scarcity premia on GPUs, HBM
Critical mineral prices > Cost per unit of compute : + :
Cost per unit of compute > Demand for compute : - : price elasticity
Cost per unit of compute > Reinvestment of efficiency gains in more computing : - : cheaper compute is reinvested in bigger models
Reinvestment of efficiency gains in more computing > Demand for compute : + : rebound / Jevons
Demand for compute > Electricity consumed : + :
Installed IT capacity > Electricity consumed : + :
Server utilization > Electricity consumed : + :
Chip energy efficiency > Electricity consumed : - : per unit of compute
Model and software efficiency > Electricity consumed : - : per unit of service
PUE > Electricity consumed : + :
Electricity consumed > Peak load : + :
Installed IT capacity > Peak load : + : contracted capacity, near-flat profile
Rack power density > Peak load : + :
Rack power density > Liquid cooling share : + : above some density air cooling is no longer enough (threshold to source)
Liquid cooling share > PUE : - :
Demand for compute > Speed of load swings : + : synchronised GPU training steps swing tens of MW
Rack power density > Speed of load swings : + :
Speed of load swings > Frequency and voltage stability : - :
Planned pipeline > Certainty of future load : - : speculative and duplicate requests
Interconnection queue > Certainty of future load : - :
Disclosure rules > Certainty of future load : + :
Chip energy efficiency > Server refresh rate : + : newer chips make old ones uneconomic
Server refresh rate > Hardware purchases : + :
Server refresh rate > Hardware retirement : + :
Installed IT capacity > Hardware purchases : + : new halls must be filled
Chip and equipment supply > Hardware purchases : + : supply constraint
Hardware purchases > Hardware kept in use : + : inflow to in-use stock
Hardware retirement > Hardware kept in use : - : outflow from in-use stock
Hardware kept in use > Hardware retirement : + : bigger fleet, more retirements
Hardware purchases > Embodied CO2 : + :
Hardware purchases > Semiconductors and memory : + :
Hardware purchases > Gallium : + : GaN power, photonics
Hardware purchases > Rare earths : + : HDD magnets, fans
Hardware purchases > Copper and aluminium : + :
Hardware purchases > Water embedded in hardware : + : fab ultrapure water
Hardware purchases > Supply-chain employment : + :
Capacity under construction > Embodied CO2 : + : concrete, steel
Installed IT capacity > Copper and aluminium : + : busbars, cable, transformers
Installed IT capacity > Battery minerals : + : UPS and BESS
Renewable generation and storage > Battery minerals : + :
Gallium > Critical mineral prices : + :
Rare earths > Critical mineral prices : + :
Copper and aluminium > Critical mineral prices : + :
Battery minerals > Critical mineral prices : + :
Gallium > Mining pressure on land and communities : + :
Rare earths > Mining pressure on land and communities : + :
Copper and aluminium > Mining pressure on land and communities : + :
Battery minerals > Mining pressure on land and communities : + :
Semiconductors and memory > Supplier concentration : + : demand flows to a few fabs and HBM makers
Supplier concentration > Exposure to supply shocks : + :
Openness of trade in minerals and equipment > Chip and equipment supply : + :
Exposure to supply shocks > Chip and equipment supply : - :
Hardware retirement > Electronic waste : + :
Hardware retirement > Material recovery from retired hardware : + :
Critical mineral prices > Material recovery from retired hardware : + : recovery pays when prices rise
Material recovery from retired hardware > Electronic waste : - :
Material recovery from retired hardware > Secondary material supply : + :
Secondary material supply > Mining pressure on land and communities : - :
Secondary material supply > Exposure to supply shocks : - :
Electronic waste > Waste traded across borders : + :
Electronic waste > Hazardous waste : + :
Electronic waste > Contamination at disposal sites : + D :
Waste traded across borders > Distribution of exposure across places and groups : + : burdens exported
Copper and aluminium > Availability of grid equipment : - : competition for the same metals
Peak load > Utility grid investment : + :
Utility grid investment > Availability of grid equipment : - : transformer and breaker backlogs
Utility grid investment > Copper and aluminium : + :
Availability of grid equipment > Transmission capacity : + D :
Availability of grid equipment > Substation and distribution capacity : + D :
Utility grid investment > Transmission capacity : + D :
Utility grid investment > Substation and distribution capacity : + D :
Utility grid investment > Utility rate base : + :
Utility grid investment > Land held for power lines and plants : + :
Utility rate base > Household electricity bills : + :
Utility rate base > Utility financial health : + : regulated return on assets
Utility financial health > Utility grid investment : + :
Stranded-cost exposure > Utility financial health : - :
Planned pipeline > Interconnection queue : + :
Peak load > Interconnection queue : + :
Interconnection queue > Grid connection wait time : + :
Transmission capacity > Grid connection wait time : - :
Substation and distribution capacity > Grid connection wait time : - :
Flexibility available to grid operators > Grid connection wait time : - : flexible / curtailable connections
Grid connection wait time > Power availability at site : - :
Grid connection wait time > Generation outside the public grid : + : bring-your-own-power
Generation outside the public grid > Power availability at site : + :
Generation outside the public grid > Natural gas demand : + :
Generation outside the public grid > Nitrogen oxides : + :
Generation outside the public grid > Continuous sound level : + :
Generation outside the public grid > Low-frequency sound : + :
Generation outside the public grid > Clarity about who has authority : - : regulatory grey zone between utility and air permits
Generation outside the public grid > Distribution of exposure across places and groups : + :
Power availability at site > Siting attractiveness : + :
Peak load > Connection headroom for other users : - :
Connection headroom for other users > Room for other businesses to grow : + :
Peak load > Reserve margin : - :
Flexibility available to grid operators > Reserve margin : + :
Reserve margin > Capacity price : - :
Reserve margin > Regional self-sufficiency in power : + :
Reserve margin > Resilience to extreme heat : + :
Peak load > Resilience to extreme heat : - :
Demand response by data centers > Flexibility available to grid operators : + :
Demand response by data centers > Diesel stored and burned : + : if curtailment runs on backup gensets
Large-load tariffs > Demand response by data centers : + :
Large-load tariffs > Share of grid costs carried by other customers : - :
Large-load tariffs > Siting attractiveness : - :
Frequency and voltage stability > Large-load tariffs : - : instability prompts ride-through and interconnection rules
Installed IT capacity > Diesel stored and burned : + : backup gensets, monthly tests
Diesel stored and burned > Nitrogen oxides : + :
Diesel stored and burned > Fine particulate matter : + :
Diesel stored and burned > Carbon monoxide : + :
Diesel stored and burned > Sulfur dioxide : + :
Diesel stored and burned > Fuel and oil contamination : + :
Diesel stored and burned > Intermittent sound : + :
Diesel stored and burned > Fire risk : + :
Electricity consumed > Gas generation : + : gas is the usual marginal / new-build resource
Electricity consumed > Coal generation : + : delayed coal retirements
Gas generation > Natural gas demand : + :
Natural gas demand > Methane : + : upstream leakage
Natural gas demand > Wholesale energy price : + : gas sets the marginal price
Natural gas demand > Exposure to supply shocks : + :
Peak load > Wholesale energy price : + :
Renewable generation and storage > Wholesale energy price : - :
Renewable generation and storage > Gas generation : - :
Clean firm generation (nuclear, geothermal) > Gas generation : - :
Clean energy procurement > Renewable generation and storage : + :
Clean energy procurement > Clean firm generation (nuclear, geothermal) : + :
Clean energy procurement > Corporate climate targets : + : market-based accounting
Renewable generation and storage > Land held for power lines and plants : + :
Renewable generation and storage > Regional self-sufficiency in power : + :
Gas generation > Operational CO2 : + :
Coal generation > Operational CO2 : + :
Gas generation > Nitrogen oxides : + :
Coal generation > Sulfur dioxide : + :
Coal generation > Fine particulate matter : + :
Gas generation > Water embedded in electricity : + :
Coal generation > Water embedded in electricity : + :
Clean firm generation (nuclear, geothermal) > Water embedded in electricity : + :
Gas generation > Water temperature : + : thermal discharge
Gas generation > Stranded-cost exposure : + : long-lived plants for uncertain load
Certainty of future load > Stranded-cost exposure : - :
Wholesale energy price > Household electricity bills : + :
Capacity price > Household electricity bills : + :
Share of grid costs carried by other customers > Household electricity bills : + :
Household electricity bills > Large-load tariffs : + : regulators respond to ratepayer pressure
Household electricity bills > Public opinion : - :
Household electricity bills > Stress and anxiety : + :
Household electricity bills > Match between who benefits and who bears costs : - :
Wholesale energy price > Siting attractiveness : - :
Operational CO2 > Atmospheric greenhouse gas stock : + :
Embodied CO2 > Atmospheric greenhouse gas stock : + :
Methane > Atmospheric greenhouse gas stock : + :
Atmospheric greenhouse gas stock > Climate change : + D :
Climate change > PUE : + : hotter ambient air means more cooling energy
Climate change > Drought and water scarcity : + :
Climate change > Resilience to extreme heat : - :
Climate change > Peak-day water demand : + :
Operational CO2 > State and national climate targets : - :
Operational CO2 > Corporate climate targets : - :
Embodied CO2 > Corporate climate targets : - : Scope 3
Corporate climate targets > Clean energy procurement : - : falling progress triggers procurement
Corporate climate targets > Fit between official metrics and lived experience : - : paper progress vs local grid reality
State and national climate targets > Clean energy standards : - : falling progress prompts policy
Clean energy standards > Renewable generation and storage : + :
Clean energy standards > Clean firm generation (nuclear, geothermal) : + :
Clean energy standards > Coal generation : - :
Energy saved in other sectors > State and national climate targets : + :
Energy demand induced elsewhere > State and national climate targets : - :
Energy saved in other sectors > Natural gas demand : - :
Energy demand induced elsewhere > Natural gas demand : + :
AI adoption and usage > Energy saved in other sectors : + : optimisation of grids, buildings, logistics
AI adoption and usage > Energy demand induced elsewhere : + : more consumption, e-commerce, extraction
AI adoption and usage > Productivity : + D :
Productivity > Regional output and income : + :
Installed IT capacity > Air temperature around sites : + : waste heat
Impervious surface > Air temperature around sites : + :
Heat reuse > Air temperature around sites : - :
Heat reuse > Energy saved in other sectors : + :
Liquid cooling share > Heat reuse : + : higher-grade heat is easier to reuse
Air temperature around sites > PUE : + :
Installed IT capacity > Water lost to evaporation : + :
Evaporative cooling share > Water lost to evaporation : + :
Evaporative cooling share > PUE : - : water-for-energy trade-off
Drought and water scarcity > Evaporative cooling share : - : shift to dry / closed-loop cooling
Water lost to evaporation > Municipal supply drawn : + :
Water lost to evaporation > Peak-day water demand : + :
Water lost to evaporation > Salinity and dissolved solids : + : blowdown concentrates solids
Evaporative cooling share > Treatment chemicals and biocides : + :
Treatment chemicals and biocides > Metals in discharge water : + : zinc / copper corrosion inhibitors
Treatment chemicals and biocides > Wastewater plant load : + :
Salinity and dissolved solids > Wastewater plant load : + :
Wastewater plant load > Public service and infrastructure spending : + :
Reclaimed water in use > Municipal supply drawn : - :
Water price > Reclaimed water in use : + :
Water price > Siting attractiveness : - :
Municipal supply drawn > Utility supply capacity : - : remaining headroom
Municipal supply drawn > Groundwater level : - :
Municipal supply drawn > River and stream flow : - :
Municipal supply drawn > Allocation among water users : - : less for farms and households
Municipal supply drawn > Public service and infrastructure spending : + :
Utility supply capacity > Water price : - :
Utility supply capacity > Room for other businesses to grow : + :
Peak-day water demand > Utility supply capacity : - :
Water embedded in electricity > River and stream flow : - :
Water embedded in hardware > Drought and water scarcity : + : in water-stressed fab regions
Drought and water scarcity > Chip and equipment supply : - :
Drought and water scarcity > Water price : + :
Groundwater level > Drought and water scarcity : - :
Groundwater recharge > Groundwater level : + :
Allocation among water users > Conflict and organised opposition : - :
Installed IT capacity > Water temperature : + : warm discharge
Water temperature > Birds and wildlife : - : aquatic life
Fuel and oil contamination > Exposure to hazardous materials : + :
Capacity under construction > Sediment and runoff : + :
Impervious surface > Sediment and runoff : + :
Sediment and runoff > Wetlands and streams : - :
Impervious surface > Groundwater recharge : - :
Capacity under construction > Farmland : - :
Capacity under construction > Forest and green space : - :
Capacity under construction > Wetlands and streams : - :
Capacity under construction > Impervious surface : + :
Capacity under construction > Reused industrial land : + : brownfield sites
Capacity under construction > Archaeological sites : - :
Capacity under construction > Cemeteries : - :
Capacity under construction > Historic landscapes and viewsheds : - :
Capacity under construction > Visual character : - :
Capacity under construction > Public access to open space : - :
Capacity under construction > Road traffic : + :
Capacity under construction > Duration of construction : + :
Capacity under construction > Intermittent sound : + :
Capacity under construction > Construction employment : + :
Capacity under construction > Land availability : - : parcels used up
Land held for power lines and plants > Farmland : - :
Land held for power lines and plants > Habitat extent and connectivity : - :
Land held for power lines and plants > Visual character : - :
Land held for power lines and plants > Security of land tenure : - : eminent domain
Land held for power lines and plants > Birds and wildlife : - : collisions
Forest and green space > Habitat extent and connectivity : + :
Wetlands and streams > Habitat extent and connectivity : + :
Farmland > Rural or residential character : + :
Farmland > Regional identity : + :
Habitat extent and connectivity > Birds and wildlife : + :
Night-time light > Birds and wildlife : - :
Continuous sound level > Birds and wildlife : - :
Security of land tenure > Fear for the community's future : - :
Visual character > Property values : + :
Visual character > Rural or residential character : + :
Public access to open space > Use of home and outdoor space : + :
Reused industrial land > Siting attractiveness : + :
Land availability > Siting attractiveness : + :
Zoning limits and moratoria > Land availability : - :
Installed IT capacity > Continuous sound level : + : chillers, fans, transformers
Installed IT capacity > Low-frequency sound : + :
Installed IT capacity > Night-time light : + :
Duration of construction > Daily routines : - :
Duration of construction > Stress and anxiety : + :
Road traffic > Emergency vehicle access : - :
Road traffic > Fine particulate matter : + :
Road traffic > Daily routines : - :
Continuous sound level > Sleep : - :
Low-frequency sound > Sleep : - :
Low-frequency sound > Stress and anxiety : + :
Intermittent sound > Sleep : - :
Night-time light > Sleep : - :
Night-time light > Rural or residential character : - :
Continuous sound level > Use of home and outdoor space : - :
Continuous sound level > Property values : - :
Sleep > Stress and anxiety : - :
Use of home and outdoor space > Stress and anxiety : - :
Daily routines > Stress and anxiety : - :
Stress and anxiety > Conflict and organised opposition : + :
Nitrogen oxides > Respiratory illness : + :
Fine particulate matter > Respiratory illness : + :
Sulfur dioxide > Respiratory illness : + :
Carbon monoxide > Respiratory illness : + :
Fine particulate matter > Premature death : + :
Resilience to extreme heat > Premature death : - : heat-wave blackouts
Respiratory illness > Cost of health damage : + :
Premature death > Cost of health damage : + :
Cost of health damage > Match between who benefits and who bears costs : - :
Installed IT capacity > Fire risk : + : lithium-ion UPS / BESS
Emergency vehicle access > Fire risk : - :
Fire risk > Exposure to hazardous materials : + :
Fire risk > Public service and infrastructure spending : + : fire / hazmat capacity
Hazardous waste > Exposure to hazardous materials : + :
Contamination at disposal sites > Exposure to hazardous materials : + :
Exposure to hazardous materials > Distribution of exposure across places and groups : + :
Bargaining power relative to developers > Distribution of exposure across places and groups : - : burdens land on low-power places
Attention to cumulative and regional effects > Distribution of exposure across places and groups : - :
Distribution of exposure across places and groups > Match between who benefits and who bears costs : - :
Installed IT capacity > Operations employment : + : small per MW
Construction employment > Availability of skilled trades : - : short-run drain on electricians, linemen
Construction employment > Hope for jobs and renewal : + :
Construction employment > Regional output and income : + :
Operations employment > Regional output and income : + :
Operations employment > Job quality and local share of jobs : + :
Availability of skilled trades > Installed IT capacity : + : speeds commissioning
Availability of skilled trades > Room for other businesses to grow : + :
Job quality and local share of jobs > Sense that promises are kept : + :
Job quality and local share of jobs > Hope for jobs and renewal : + :
Installed IT capacity > Local tax revenue : + : property and equipment tax
Data center tax incentives > State tax revenue forgone : + :
Data center tax incentives > Siting attractiveness : + :
Data center tax incentives > Value kept by host regions and countries : - :
State tax revenue forgone > Public service and infrastructure spending : - :
Local tax revenue > Fiscal dependence on one industry : + :
Local tax revenue > Public service and infrastructure spending : + :
Local tax revenue > Public opinion : + :
Local tax revenue > Value kept by host regions and countries : + :
Fiscal dependence on one industry > Data center tax incentives : + : protect the tax base
Fiscal dependence on one industry > Zoning limits and moratoria : - :
Fiscal dependence on one industry > Local control over land use : - :
Capital investment > Regional output and income : + :
Capital investment > Investment share of growth : + :
Investment share of growth > Investor expectations : + : macro narrative
Regional output and income > Property values : + :
Property values > Local tax revenue : + :
Installed IT capacity > Connectivity : + : fibre, IXPs
Connectivity > Siting attractiveness : + : latency and ecosystem
Bargaining power relative to developers > Value kept by host regions and countries : + :
Bargaining power relative to developers > Community benefit agreements : + :
Value kept by host regions and countries > Match between who benefits and who bears costs : + :
Community benefit agreements > Sense that promises are kept : + :
Community benefit agreements > Value kept by host regions and countries : + :
Developer secrecy > Public availability of project information : - :
Developer secrecy > Public availability of contract terms : - :
Developer secrecy > Trust in developers and officials : - :
Developer secrecy > Visibility of infrastructure and its labour : - :
Developer secrecy > Community say in decisions : - :
Disclosure rules > Public data on energy and water use : + :
Disclosure rules > Public availability of contract terms : + :
Disclosure rules > Developer secrecy : - :
Public availability of project information > Community say in decisions : + :
Public availability of project information > Quality of information in public debate : + :
Public availability of contract terms > Bargaining power relative to developers : + :
Public availability of contract terms > Trust in developers and officials : + :
Public data on energy and water use > Fit between official metrics and lived experience : + :
Public data on energy and water use > Visibility of infrastructure and its labour : + :
Public data on energy and water use > Certainty of future load : + :
Visibility of infrastructure and its labour > Quality of information in public debate : + :
Visibility of infrastructure and its labour > Physical attack on facilities : + : transparency vs security tension
Quality of information in public debate > Attention to cumulative and regional effects : + :
Fit between official metrics and lived experience > Trust in developers and officials : + :
Sense that promises are kept > Trust in developers and officials : + :
Community say in decisions > Trust in developers and officials : + :
Community say in decisions > Attention to cumulative and regional effects : + :
Clarity about who has authority > Community say in decisions : + :
Local control over land use > Zoning limits and moratoria : + :
Attention to cumulative and regional effects > Zoning limits and moratoria : + : regional siting rules
Trust in developers and officials > Conflict and organised opposition : - :
Match between who benefits and who bears costs > Conflict and organised opposition : - :
Hope for jobs and renewal > Public opinion : + :
Fear for the community's future > Public opinion : - :
Fear for the community's future > Conflict and organised opposition : + :
Rural or residential character > Fear for the community's future : - :
Regional identity > Fear for the community's future : - :
Relation to earlier industrial and extractive history > Fear for the community's future : + : 'we've seen this before'
Relation to earlier industrial and extractive history > Hope for jobs and renewal : + : post-industrial towns seek renewal
Public opinion > Conflict and organised opposition : - :
Conflict and organised opposition > Zoning limits and moratoria : + :
Conflict and organised opposition > Permitting speed : - : hearings, lawsuits
Conflict and organised opposition > Disclosure rules : + :
Conflict and organised opposition > Developer secrecy : + : developers hide plans to avoid opposition
Conflict and organised opposition > Bargaining power relative to developers : + :
Conflict and organised opposition > Planned pipeline : - : cancellations
Zoning limits and moratoria > Permitting speed : - :
Installed IT capacity > Physical attack on facilities : + : higher-value target
Physical attack on facilities > Developer secrecy : + : security justifies opacity
Installed IT capacity > Cyberattack on energy systems : + : larger attack surface
Flexibility available to grid operators > Cyberattack on energy systems : + : more digitally controlled load
Cyberattack on energy systems > Frequency and voltage stability : - :
Peak load > Regional self-sufficiency in power : - :
Regional self-sufficiency in power > Exposure to supply shocks : - :
National compute capacity > Supplier concentration : + : more demand on the same few suppliers
"""

edges = []
lab2id = {n["label"]: k for k, n in nodes.items()}
errs = []
for ln in LINKS.strip().splitlines():
    parts = [p.strip() for p in ln.split(":", 2)]
    src, dst = [s.strip() for s in parts[0].split(">")]
    sign = parts[1].split()[0]
    delay = "D" in parts[1]
    for x in (src, dst):
        if x not in lab2id: errs.append(x)
    edges.append(dict(source=lab2id.get(src), target=lab2id.get(dst), sign=sign, delay=delay, note=parts[2]))
assert not errs, ("unknown labels", sorted(set(errs)))
pairs = collections.Counter((e["source"], e["target"]) for e in edges)
assert all(v == 1 for v in pairs.values()), [k for k, v in pairs.items() if v > 1]
emap = {(e["source"], e["target"]): e for e in edges}

# ---- named feedback loops (type is computed from link signs and checked)
LOOPS = [
 ("R1", "AI boom flywheel", "R", ["AI capability", "AI adoption and usage", "AI and cloud revenue", "Investor expectations", "Data center capex", "Planned pipeline", "Capacity under construction", "Installed IT capacity", "National compute capacity"],
  "Better models drive use and revenue, which validates investor belief, funds capex, and adds the compute that trains the next models. The engine of the build-out; long delays (permitting, construction, training) make it prone to overshoot."),
 ("R2", "Scale and efficiency rebound", "R", ["Cost per unit of compute", "Reinvestment of efficiency gains in more computing", "Demand for compute", "Planned pipeline", "Capacity under construction", "Installed IT capacity"],
  "Scale and efficiency cut the cost of compute; cheaper compute is reinvested in larger models and more usage, so total electricity rises even as energy per operation falls (Jevons)."),
 ("R3", "Hub clustering", "R", ["Installed IT capacity", "Connectivity", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "Fibre, interconnection points and a supplier ecosystem make existing hubs more attractive, concentrating load and local impacts."),
 ("R4", "Fiscal capture", "R", ["Installed IT capacity", "Local tax revenue", "Fiscal dependence on one industry", "Data center tax incentives", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "Tax revenue makes the host dependent on the industry, which sustains incentives and weakens appetite to restrict it, bringing more projects."),
 ("R5", "Secrecy–distrust spiral", "R", ["Developer secrecy", "Trust in developers and officials", "Conflict and organised opposition"],
  "NDAs and code-named projects erode trust; opposition grows; developers become more secretive to avoid it."),
 ("R6", "Bring-your-own-power", "R", ["Peak load", "Interconnection queue", "Grid connection wait time", "Generation outside the public grid", "Power availability at site", "Siting attractiveness", "Planned pipeline", "Capacity under construction", "Installed IT capacity"],
  "Grid queues push developers to on-site gas turbines, which restores power availability and lets the build-out continue – moving emissions, noise and regulatory ambiguity to the fence line."),
 ("R7", "Warming raises cooling load", "R", ["Electricity consumed", "Gas generation", "Operational CO2", "Atmospheric greenhouse gas stock", "Climate change", "PUE"],
  "Fossil-supplied load adds to warming; hotter ambient air raises cooling energy. Weak and slow globally, but locally visible in heat waves."),
 ("R8", "Utility rate-base growth", "R", ["Utility grid investment", "Utility rate base", "Utility financial health"],
  "Regulated utilities earn a return on capital, so large-load growth is an incentive to build – costs that ratepayers may carry if load does not materialise."),
 ("R9", "Circular supply security", "R", ["Hardware purchases", "Hardware kept in use", "Hardware retirement", "Material recovery from retired hardware", "Secondary material supply", "Exposure to supply shocks", "Chip and equipment supply"],
  "Recovering metals from retired servers lowers supply-shock exposure, easing hardware supply. Today this loop is weak because recovery rates for Ga, REE and other critical metals are low."),
 ("R10", "Jobs promise", "R", ["Hope for jobs and renewal", "Public opinion", "Conflict and organised opposition", "Zoning limits and moratoria", "Land availability", "Siting attractiveness", "Planned pipeline", "Capacity under construction", "Construction employment"],
  "Construction jobs build hope and support, easing approvals for further projects. Can flip if operations jobs (few per MW) fall short of promises."),
 ("B1", "Grid queue brake", "B", ["Installed IT capacity", "Peak load", "Interconnection queue", "Grid connection wait time", "Power availability at site", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "Load fills the interconnection queue; waits lengthen; sites lose power availability and the pipeline slows. The main physical brake on growth today."),
 ("B2", "Power price brake", "B", ["Installed IT capacity", "Peak load", "Wholesale energy price", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "Rising wholesale prices make a region less attractive for new load."),
 ("B3", "Ratepayer backlash", "B", ["Household electricity bills", "Large-load tariffs", "Share of grid costs carried by other customers"],
  "Rising bills push regulators to large-load tariffs that shift grid costs back to data centers."),
 ("B4", "Tariffs slow growth", "B", ["Installed IT capacity", "Peak load", "Utility grid investment", "Utility rate base", "Household electricity bills", "Large-load tariffs", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "The same ratepayer response also makes a region less attractive, slowing new projects."),
 ("B5", "Neighbour pushback", "B", ["Installed IT capacity", "Continuous sound level", "Sleep", "Stress and anxiety", "Conflict and organised opposition", "Zoning limits and moratoria", "Land availability", "Siting attractiveness", "Planned pipeline", "Capacity under construction"],
  "Noise, light and disruption mobilise residents into opposition, leading to zoning limits and moratoria."),
 ("B6", "Water scarcity shifts cooling", "B", ["Water lost to evaporation", "Municipal supply drawn", "Groundwater level", "Drought and water scarcity", "Evaporative cooling share"],
  "Evaporative cooling draws down local water; scarcity pushes operators to dry or closed-loop cooling – which raises PUE and electricity use (problem shifting to the grid)."),
 ("B7", "Corporate clean procurement", "B", ["Clean energy procurement", "Renewable generation and storage", "Gas generation", "Operational CO2", "Corporate climate targets"],
  "Falling progress toward corporate targets triggers PPAs and clean firm deals. Strength depends on additionality and hourly matching."),
 ("B8", "Public clean energy standards", "B", ["Operational CO2", "State and national climate targets", "Clean energy standards", "Coal generation"],
  "Missed state targets prompt clean energy standards that retire coal – if policy responds."),
 ("B9", "Leverage limits capex", "B", ["Data center capex", "Debt and financial exposure", "Cost of capital"],
  "Debt-financed build-out raises risk premia and the cost of capital, slowing further capex – the financial brake on overshoot."),
 ("B10", "Mineral cost brake", "B", ["Hardware purchases", "Gallium", "Critical mineral prices", "Cost per unit of compute", "Reinvestment of efficiency gains in more computing", "Demand for compute", "Planned pipeline", "Capacity under construction", "Installed IT capacity"],
  "Hardware demand tightens critical-mineral markets, raising compute costs and damping demand."),
 ("B11", "Fab water constraint", "B", ["Hardware purchases", "Water embedded in hardware", "Drought and water scarcity", "Chip and equipment supply"],
  "Chip fabs in water-stressed regions compete for water; droughts constrain chip supply."),
 ("B12", "Disclosure rebuilds trust", "B", ["Conflict and organised opposition", "Disclosure rules", "Public availability of contract terms", "Trust in developers and officials"],
  "Opposition wins disclosure rules; published contracts rebuild trust and dampen conflict."),
 ("B13", "Security–transparency tension", "B", ["Developer secrecy", "Visibility of infrastructure and its labour", "Physical attack on facilities"],
  "Attack risk justifies secrecy, which lowers visibility (and attack risk) – while feeding the R5 distrust spiral."),
 ("B14", "Skilled-trades bottleneck", "B", ["Capacity under construction", "Construction employment", "Availability of skilled trades", "Installed IT capacity", "Connectivity", "Siting attractiveness", "Planned pipeline"],
  "A construction boom drains electricians and linemen, slowing commissioning and, through it, the attraction of new projects. Also crowds out housing, grid and factory construction."),
]
loops = []
for lid, name, typ, path, story in LOOPS:
    ids = [lab2id[p] for p in path]
    neg = 0
    for a, b in zip(ids, ids[1:] + ids[:1]):
        e = emap.get((a, b))
        assert e, (lid, nodes[a]["label"], "->", nodes[b]["label"])
        neg += e["sign"] == "-"
    calc = "R" if neg % 2 == 0 else "B"
    assert calc == typ, (lid, calc, typ)
    loops.append(dict(id=lid, name=name, type=calc, nodes=ids, story=story))

# ---- physical components -> impacts (for the zoom-in garden)
COMPONENTS = {
 "Site and building": {
  "Site works and land clearing": "Farmland|Forest and green space|Wetlands and streams|Impervious surface|Sediment and runoff|Habitat extent and connectivity|Archaeological sites|Cemeteries|Road traffic|Duration of construction|Intermittent sound|Construction employment|Embodied CO2",
  "Building shell (concrete, steel)": "Embodied CO2|Visual character|Historic landscapes and viewsheds|Impervious surface|Construction employment|Property values|Local tax revenue|Availability of skilled trades",
  "Perimeter, security and lighting": "Night-time light|Birds and wildlife|Visual character|Public access to open space|Physical attack on facilities|Visibility of infrastructure and its labour",
 },
 "Power": {
  "Grid interconnection and substation": "Substation and distribution capacity|Connection headroom for other users|Peak load|Availability of grid equipment|Copper and aluminium|Land held for power lines and plants|Low-frequency sound|Interconnection queue",
  "New transmission lines": "Transmission capacity|Land held for power lines and plants|Security of land tenure|Visual character|Birds and wildlife|Household electricity bills|Share of grid costs carried by other customers|Copper and aluminium|Historic landscapes and viewsheds",
  "Transformers and switchgear": "Availability of grid equipment|Copper and aluminium|Continuous sound level|Low-frequency sound|Fire risk",
  "UPS and battery storage": "Battery minerals|Fire risk|Exposure to hazardous materials|Hazardous waste|Frequency and voltage stability|Flexibility available to grid operators",
  "Backup diesel generators": "Diesel stored and burned|Nitrogen oxides|Fine particulate matter|Carbon monoxide|Sulfur dioxide|Intermittent sound|Low-frequency sound|Fuel and oil contamination|Fire risk|Respiratory illness|Distribution of exposure across places and groups",
  "On-site gas turbines / fuel cells": "Generation outside the public grid|Natural gas demand|Methane|Operational CO2|Nitrogen oxides|Continuous sound level|Low-frequency sound|Clarity about who has authority|Regional self-sufficiency in power|Stranded-cost exposure",
  "On-site solar and storage": "Renewable generation and storage|Battery minerals|Land held for power lines and plants|Corporate climate targets",
 },
 "IT equipment": {
  "GPU / accelerator servers": "Electricity consumed|Peak load|Speed of load swings|Semiconductors and memory|Gallium|Embodied CO2|Water embedded in hardware|Electronic waste|Supplier concentration|Openness of trade in minerals and equipment|National compute capacity|Local tax revenue|Hardware kept in use|Capital investment|Debt and financial exposure",
  "CPU servers and storage": "Electricity consumed|Semiconductors and memory|Rare earths|Embodied CO2|Electronic waste|Hardware kept in use|Hazardous waste",
  "Networking and fibre": "Connectivity|Copper and aluminium|Gallium|Semiconductors and memory|Electronic waste",
 },
 "Cooling and water": {
  "Chillers and air handlers": "Electricity consumed|Peak load|Continuous sound level|Low-frequency sound|Air temperature around sites|Operational CO2",
  "Evaporative cooling towers": "Water lost to evaporation|Municipal supply drawn|Peak-day water demand|Salinity and dissolved solids|Treatment chemicals and biocides|Metals in discharge water|Wastewater plant load|Continuous sound level|Allocation among water users|Groundwater level",
  "Dry coolers": "Electricity consumed|Peak load|Continuous sound level|Air temperature around sites|Resilience to extreme heat",
  "Direct-to-chip / immersion liquid cooling": "Electricity consumed|Exposure to hazardous materials|Hazardous waste|Energy saved in other sectors",
  "Water treatment and discharge": "Treatment chemicals and biocides|Metals in discharge water|Salinity and dissolved solids|Water temperature|Wastewater plant load|Reclaimed water in use",
  "Heat rejection and reuse": "Energy saved in other sectors|Air temperature around sites|Water temperature",
 },
 "People, contracts and end of life": {
  "Operations staff": "Operations employment|Job quality and local share of jobs|Road traffic|Visibility of infrastructure and its labour",
  "Development agreements (NDAs, tax deals, CBAs)": "Public availability of project information|Public availability of contract terms|State tax revenue forgone|Local tax revenue|Trust in developers and officials|Bargaining power relative to developers|Sense that promises are kept|Clarity about who has authority|Community say in decisions|Value kept by host regions and countries",
  "Metering and reporting": "Public data on energy and water use|Fit between official metrics and lived experience|Quality of information in public debate|Corporate climate targets|Certainty of future load",
  "Decommissioning and IT asset disposition": "Electronic waste|Hardware kept in use|Waste traded across borders|Contamination at disposal sites|Hazardous waste|Mining pressure on land and communities",
 },
}
components = []
for sys_, comps in COMPONENTS.items():
    for c, labs in comps.items():
        ids = []
        for l in labs.split("|"):
            assert l in lab2id, ("component impact", c, l)
            ids.append(lab2id[l])
        components.append(dict(system=sys_, name=c, impacts=ids))

# ---- stock-and-flow panels. Each panel: stocks (S), clouds (C) on a grid; flows between them with drivers.
SFD = [
 dict(id="capacity", title="Data center capacity (MW)", note="Ageing chain from announcement to retirement. Delays here drive overshoot.",
  nodes=[("c0","C",0,0),("pipe","S",1,0,"Planned pipeline"),("uc","S",2,0,"Capacity under construction"),("inst","S",3,0,"Installed IT capacity"),("c1","C",4,0),("cx","C",1,1)],
  flows=[("c0","pipe","Project announcements",["Investor expectations","Demand for compute","Siting attractiveness"]),
         ("pipe","uc","Construction starts",["Permitting speed","Power availability at site","Zoning limits and moratoria"]),
         ("uc","inst","Commissioning",["Availability of skilled trades","Availability of grid equipment"]),
         ("inst","c1","Decommissioning",["Server refresh rate"]),
         ("pipe","cx","Cancellations",["Conflict and organised opposition","Grid connection wait time","Cost of capital"])]),
 dict(id="hardware", title="Hardware and materials (dMFA)", note="Units or tonnes of metal. Recovery closes the loop back to supply.",
  nodes=[("c0","C",0,0),("use","S",1,0,"Hardware kept in use"),("ret","S",2,0,"Retired hardware (stock)"),("sec","S",3,0,"Secondary material supply"),("land","C",2,1),("c1","C",4,0)],
  flows=[("c0","use","Hardware purchases",["Installed IT capacity","Server refresh rate","Chip and equipment supply"]),
         ("use","ret","Hardware retirement",["Server refresh rate","Chip energy efficiency"]),
         ("ret","use","Reuse and refurbishment",["Critical mineral prices"]),
         ("ret","sec","Material recovery",["Material recovery from retired hardware","Critical mineral prices"]),
         ("ret","land","Landfill and export (e-waste)",["Electronic waste","Waste traded across borders"]),
         ("sec","c1","Re-entry into manufacturing",["Exposure to supply shocks"])]),
 dict(id="grid", title="Grid access and generation", note="GW of queued load, generation capacity by type, and the utility rate base ($).",
  nodes=[("c0","C",0,0),("q","S",1,0,"Interconnection queue"),("conn","S",2,0,"Connected large load"),("cw","C",1,1),
         ("c2","C",0,2),("gen","S",1,2,"Generation capacity by type"),("c3","C",2,2),
         ("c4","C",0,3),("rb","S",1,3,"Utility rate base"),("c5","C",2,3)],
  flows=[("c0","q","Interconnection requests",["Planned pipeline","Peak load"]),
         ("q","conn","Connection approvals",["Transmission capacity","Substation and distribution capacity","Flexibility available to grid operators"]),
         ("q","cw","Withdrawn requests",["Grid connection wait time","Large-load tariffs"]),
         ("c2","gen","Capacity additions",["Peak load","Clean energy procurement","Clean energy standards"]),
         ("gen","c3","Retirements",["Clean energy standards","Electricity consumed (delays)"]),
         ("c4","rb","Utility grid investment",["Peak load","Utility financial health"]),
         ("rb","c5","Depreciation recovered through bills",["Household electricity bills","Large-load tariffs"])]),
 dict(id="carbon", title="Carbon", note="Emissions are flows; the atmosphere integrates them.",
  nodes=[("c0","C",0,1),("ghg","S",1,1,"Atmospheric greenhouse gas stock"),("c1","C",2,1),("c2","C",1,0),("c3","C",1,2)],
  flows=[("c0","ghg","Operational emissions",["Gas generation","Coal generation","Generation outside the public grid","Diesel stored and burned"]),
         ("c2","ghg","Embodied emissions",["Hardware purchases","Capacity under construction"]),
         ("c3","ghg","Methane leakage",["Natural gas demand"]),
         ("ghg","c1","Natural removal (very slow)",[])]),
 dict(id="water", title="Water", note="Aquifer storage with competing withdrawals; reclaimed water substitutes for potable draw.",
  nodes=[("c0","C",0,0),("aq","S",1,0,"Groundwater level (aquifer storage)"),("c1","C",2,0),("c2","C",2,1)],
  flows=[("c0","aq","Groundwater recharge",["Impervious surface","Climate change"]),
         ("aq","c1","Data center withdrawals",["Water lost to evaporation","Evaporative cooling share","Reclaimed water in use"]),
         ("aq","c2","Other users' withdrawals",["Allocation among water users","Drought and water scarcity"])]),
 dict(id="land", title="Land", note="Conversion is effectively irreversible on planning timescales.",
  nodes=[("und","S",0,0,"Undeveloped land (farm, forest, wetland)"),("dc","S",1,0,"Land developed for data centers"),("pl","S",1,1,"Land held for power lines and plants")],
  flows=[("und","dc","Site conversion",["Capacity under construction","Zoning limits and moratoria","Reused industrial land"]),
         ("und","pl","Corridor acquisition",["Utility grid investment","Renewable generation and storage","Security of land tenure"])]),
 dict(id="labour", title="Skilled workforce", note="Electricians, linemen, pipefitters shared with housing, grid and manufacturing.",
  nodes=[("c0","C",0,0),("tr","S",1,0,"Availability of skilled trades"),("c1","C",2,0),("c2","C",1,1)],
  flows=[("c0","tr","Training and apprenticeships",["Construction employment (long run)","Public service and infrastructure spending"]),
         ("tr","c1","Absorbed by data center construction",["Construction employment"]),
         ("tr","c2","Retirement and exit",[])]),
 dict(id="fiscal", title="Local tax base", note="Server equipment depreciates much faster than buildings, so equipment tax revenue can fall off unless hardware is refreshed (schedule to source).",
  nodes=[("c0","C",0,0),("tb","S",1,0,"Taxable data center property"),("c1","C",2,0),("c2","C",1,1)],
  flows=[("c0","tb","New taxable buildings and equipment",["Installed IT capacity","Hardware purchases"]),
         ("tb","c1","Equipment depreciation",["Server refresh rate"]),
         ("tb","c2","Abatements",["Data center tax incentives"])]),
 dict(id="finance", title="Capital and expectations", note="Soft stocks that drive capex; the overshoot risk lives here.",
  nodes=[("c0","C",0,0),("ie","S",1,0,"Investor expectations"),("c1","C",2,0),("c2","C",0,1),("debt","S",1,1,"Debt and financial exposure"),("c3","C",2,1)],
  flows=[("c0","ie","Narrative building",["AI and cloud revenue","Investment share of growth"]),
         ("ie","c1","Disappointment",["Server utilization","Cost of capital"]),
         ("c2","debt","Borrowing for capex",["Data center capex"]),
         ("debt","c3","Repayment from revenue",["AI and cloud revenue"])]),
 dict(id="social", title="Trust and opposition", note="Soft stocks that change slowly and gate permitting.",
  nodes=[("c0","C",0,0),("tr","S",1,0,"Trust in developers and officials"),("c1","C",2,0),("c2","C",0,1),("op","S",1,1,"Conflict and organised opposition"),("c3","C",2,1)],
  flows=[("c0","tr","Trust building",["Sense that promises are kept","Public availability of contract terms","Community say in decisions"]),
         ("tr","c1","Trust erosion",["Developer secrecy","Household electricity bills","Fit between official metrics and lived experience"]),
         ("c2","op","Mobilisation",["Stress and anxiety","Fear for the community's future","Allocation among water users"]),
         ("op","c3","Resolution or fatigue",["Community benefit agreements","Trust in developers and officials"])]),
]

model = dict(
    title="Data center system map",
    domains_order=list(dict.fromkeys(n["domain"] for n in nodes.values())),
    knowability=KNOW, nodes=list(nodes.values()), edges=edges, loops=loops,
    components=components, sfd=SFD)
json.dump(model, open("model.json", "w"), indent=1)

# Kumu / generic CSV exports
with open("nodes.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Label", "ID", "Type", "Domain", "Subgroup", "SD role", "Knowability", "Note"])
    for n in nodes.values():
        w.writerow([n["label"], n["id"], "Impact" if n["group"] == "impact" else "Driver", n["domain"], n.get("sub", ""),
                    n["role"], KNOW.get(n["know"], ""), n.get("note", "")])
with open("links.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["From", "To", "Polarity", "Delay", "Note"])
    for e in edges:
        w.writerow([nodes[e["source"]]["label"], nodes[e["target"]]["label"], e["sign"], "yes" if e["delay"] else "", e["note"]])
with open("loops.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ID", "Name", "Type", "Path", "Story"])
    for l in loops:
        w.writerow([l["id"], l["name"], "Reinforcing" if l["type"] == "R" else "Balancing",
                    " -> ".join(nodes[i]["label"] for i in l["nodes"]), l["story"]])
with open("component_impacts.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["System", "Component", "Impact", "Impact domain"])
    for c in components:
        for i in c["impacts"]:
            w.writerow([c["system"], c["name"], nodes[i]["label"], nodes[i]["domain"]])

# coverage report
deg = collections.Counter()
for e in edges: deg[e["source"]] += 1; deg[e["target"]] += 1
iso = [n["label"] for n in nodes.values() if deg[n["id"]] == 0]
inloop = set(i for l in loops for i in l["nodes"])
print(f"impacts {N_IMPACTS}, drivers {len(nodes)-N_IMPACTS}, links {len(edges)}, loops {len(loops)}, components {len(components)}")
print("isolated:", iso)
print("loop types:", collections.Counter(l["type"] for l in loops))
print("nodes in loops:", len(inloop))
# impacts with no incoming link (pure outcome-free) / no outgoing (pure endpoints)
noin = [n["label"] for n in nodes.values() if not any(e["target"] == n["id"] for e in edges)]
print("no incoming:", noin)
