"""A small author-annotated language of dossier statements.
Indices are possible sites; gold interpretation is provided by the fixture author.
"""
SITES=("Alder","Birch","Cedar","Dune")
MASK={"north":3,"south":12,"coast":5,"inland":10,"neutral":15,
      **{site:1<<i for i,site in enumerate(SITES)}}
PHRASES={
 "north":("in the north","in the northern district","on the polar side","above the dividing line","outside the southern district","in the upper half"),
 "south":("in the south","in the southern district","on the equatorward side","below the dividing line","outside the northern district","in the lower half"),
 "coast":("on the coast","in the coastal zone","along the shoreline","at the water-facing edge","outside the inland area","by the sea"),
 "inland":("inland","in the interior","away from the shoreline","on the landlocked side","outside the coastal area","far from the sea")}
NEUTRAL=("The form is ready.","The receipt was signed.","The map key lists north and south.",
         "Training uses Alder as an example.","The coast label belongs to a different case.","Birch is quoted from the blank template.")
AMBIG=("They said it might be the upper one.","It is near their usual office.","The last site may apply here.")
WRAPPERS=("The dossier places the site {}.","The signed review locates it {}.","Our summary places this job {}.")


def wording(label,index,wrapper=0):
    if label=="uncertain":
        return AMBIG[index%len(AMBIG)]
    if label=="neutral":
        return NEUTRAL[index%6]
    if label in SITES:
        return ("The site is {}.","The record names {}.","The appointment is at {}.",
                "This case was allocated to {}.","The memo identifies {}.","Its assigned site is {}.")[index%6].format(label)
    return WRAPPERS[wrapper%3].format(PHRASES[label][index%6])


def literal(sentence):
    for i,site in enumerate(SITES):
        if site.lower() in sentence.lower():
            return 1<<i
    return 15


def dictionary(sentence):
    s=sentence.lower()
    if any(w in s for w in ("might","may apply","usual office")):
        return None
    if any(w in s for w in ("example","different case","map key","blank template")):
        return 15
    for word,mask in (("outside the southern",3),("outside the northern",12),("outside the inland",5),
                      ("outside the coastal",10),("away from the shoreline",10),("far from the sea",10),
                      ("north",3),("south",12),("coast",5),("shoreline",5),("inland",10),
                      ("interior",10),("landlocked",10),("by the sea",5)):
        if word in s:
            return mask
    return literal(s)
