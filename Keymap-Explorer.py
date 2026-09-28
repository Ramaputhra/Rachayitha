
from typing import Dict, List, Tuple
ACHULU = {'a':'అ','aa':'ఆ','A':'ఆ','i':'ఇ','ii':'ఈ','I':'ఈ','u':'ఉ','uu':'ఊ','U':'ఊ','Ru':'ఋ','e':'ఎ','ee':'ఏ','E':'ఏ','ai':'ఐ','o':'ఒ','oo':'ఓ','O':'ఓ','au':'ఔ','M':'ం','H':'ః'}
HALLULU_BASE = {'k':'క','kh':'ఖ','g':'గ','gh':'ఘ','c':'చ','ch':'ఛ','j':'జ','T':'ట','Th':'ఠ','D':'డ','Dh':'ఢ','t':'త','th':'థ','d':'ద','dh':'ధ','n':'న','N':'ణ','p':'ప','ph':'ఫ','b':'బ','bh':'భ','m':'మ','y':'య','r':'ర','l':'ల','L':'ళ','v':'వ','sh':'శ','S':'శ','Sh':'ష','s':'స','h':'హ','ksh':'క్ష','kS':'క్ష','R':'ఱ'}
GUNINTHALU_MODIFIERS = {'a':('',''), 'aa':('ా','ా'), 'i':('ి','ి'), 'ii':('ీ','ీ'), 'u':('ు','ు'), 'uu':('ూ','ూ'), 'Ru':('ృ','ృ'), 'e':('ె','ె'), 'ee':('ే','ే'), 'ai':('ై','ై'), 'o':('ొ','ొ'), 'oo':('ో','ో'), 'au':('ౌ','ౌ')}
VATTULU_SAMPLE = {'kka':'క్క','kya':'క్య','kra':'క్ర','kla':'క్ల','kva':'క్వ','nna':'న్న','mma':'మ్మ','yya':'య్య','lla':'ల్ల','ksha':'క్ష','tra':'త్ర','pra':'ప్ర','sri':'శ్రీ'}

class KeyMapExplorer:
    def __init__(self, rules_path=None):
        self.rules_path = rules_path
        self.forward_map: Dict[str,str] = {}
        self.reverse_map: Dict[str,List[str]] = {}
        self.categories: Dict[str,List[Tuple[str,str]]] = {"Achulu":[], "Hallulu":[], "Guninthalu":[], "Vattulu":[]}
        self.load()
    def load(self):
        self.forward_map.update(ACHULU)
        self.forward_map.update(HALLULU_BASE)
        self.forward_map.update(VATTULU_SAMPLE)
        for eng,tel in self.forward_map.items():
            self.reverse_map.setdefault(tel, []).append(eng)
        for base_eng,base_tel in HALLULU_BASE.items():
            if len(base_eng)>2: continue
            for mod_eng,(mod_tel,_) in GUNINTHALU_MODIFIERS.items():
                if mod_eng=='a':
                    eng_key = base_eng+'a'
                else:
                    eng_key = base_eng+mod_eng
                tel = base_tel + mod_tel if mod_tel else base_tel
                self.forward_map[eng_key]=tel
                self.reverse_map.setdefault(tel, []).append(eng_key)
        for eng,tel in ACHULU.items():
            self.categories["Achulu"].append((eng,tel))
        for eng,tel in HALLULU_BASE.items():
            self.categories["Hallulu"].append((eng,tel))
        for mod_eng,(mod_tel,_) in GUNINTHALU_MODIFIERS.items():
            self.categories["Guninthalu"].append((f"k{mod_eng}", f"క{mod_tel}"))
        for eng,tel in VATTULU_SAMPLE.items():
            self.categories["Vattulu"].append((eng,tel))
    def search(self, query:str):
        query=query.lower().strip()
        results=[]
        if not query:
            for cat,items in self.categories.items():
                for eng,tel in items:
                    results.append((eng,tel,cat))
            return results
        for eng,tel in self.forward_map.items():
            if query in eng.lower() or query in tel:
                cat="Guninthalu"
                if tel in [t for _,t in self.categories["Achulu"]]: cat="Achulu"
                elif tel in [t for _,t in self.categories["Hallulu"]]: cat="Hallulu"
                elif tel in [t for _,t in self.categories["Vattulu"]]: cat="Vattulu"
                results.append((eng,tel,cat))
        seen=set(); dedup=[]
        for eng,tel,cat in results:
            if (eng,tel) not in seen:
                dedup.append((eng,tel,cat)); seen.add((eng,tel))
        return sorted(dedup, key=lambda x:(len(x[0]),x[0]))[:100]
    def reverse_lookup(self, telugu_char:str):
        return self.reverse_map.get(telugu_char,[])
    def get_stats(self):
        return {"total_achulu":len(self.categories["Achulu"]),"total_hallulu":len(self.categories["Hallulu"]),"total_guninthalu":len(HALLULU_BASE)*len(GUNINTHALU_MODIFIERS),"total_vattulu":len(self.categories["Vattulu"]),"total_mappings":len(self.forward_map)}
