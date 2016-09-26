from bs4 import BeautifulSoup
from lxml import etree as ET
import json
import string
from xml.dom import minidom
from xml.etree import ElementTree
import os
from xml.etree import ElementTree
from xml.dom import minidom


with open('author_ranges.json') as data_file:
    authors_offset = json.load(data_file)

poster_hash={}
map_author={}# Mapping a number betwwen 0-n for poster to find the priority

def m_id_return(filename,offset):
    #this method receives the offset of trigger and finds the accotiated m-ID
    for x,v in authors_offset[filename].items():
        for items in v:
            if offset>=items[0] and offset<=items[1]:
                return x


def Getting_Authors(xml_out_file):
    Train_corpus=[]
    i=0
    with open(xml_out_file,"r") as f:
        for line in f:
            soup = BeautifulSoup(line,'html.parser');
            starttag = soup.findAll("post")#finding all the post tags
            qoute_tag=soup.findAll("quote")
            for tag in starttag:
                if tag["author"] not in Train_corpus:
                    Train_corpus.append(tag["author"])
                map_author[tag["author"]]=i
                i+=1
            for tag in qoute_tag:
                try: #Some cases we dont have qauthor in quote tag, we collect all authors from text
                    if tag["orig_author"] not in Train_corpus:
                        Train_corpus.append(tag["orig_author"])
                    map_author[tag["orig_author"]]=i
                    i+=1
                except:
                    continue

    return Train_corpus



def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def find_ind(Source_str,string):
    tmp_ar=[]
    ind=0
    try:
        while Source_str.index(string,ind) :
            ind=Source_str.index(string,ind)
            tmp_ar.append(ind)
            ind=ind+len(string)
    except:
        return tmp_ar

def creat_xml_relat(ere_id,trigger,offset,length,belief_type,source,s_offset,s_length,s_ere_id):
    rltion = ET.SubElement(rltions, 'relation')
    rltion.set('ere_id',ere_id)
    trig = ET.SubElement(rltion, 'trigger')
    trig.set('offset',offset)
    trig.set('length',length)
    trig.text=trigger
    belfs = ET.SubElement(rltion, 'beliefs')
    belf = ET.SubElement(belfs, 'belief')
    belf.set('type',belief_type)
    belf.set('polarity','pos')
    belf.set('sarcasm','')
    src = ET.SubElement(belf, 'source')
    src.set('ere_id',s_ere_id)
    src.set('offset',s_offset)
    src.set('length',s_length)
    src.text=source
    return ET.tostring(rltion, pretty_print=True,with_tail=False, xml_declaration=False)

def creat_xml_event(ere_id,trigger,offset,length,belief_type,source,s_offset,s_length,s_ere_id):
    event = ET.SubElement(evnts, 'event')
    event.set('ere_id',ere_id)
    trig = ET.SubElement(event, 'trigger')
    trig.set('offset',offset)
    trig.set('length',length)
    trig.text=trigger
    belfs = ET.SubElement(event, 'beliefs')
    belf = ET.SubElement(belfs, 'belief')
    belf.set('type',belief_type)
    belf.set('polarity','pos')
    belf.set('sarcasm','')
    src = ET.SubElement(belf, 'source')
    src.set('ere_id',s_ere_id)
    src.set('offset',s_offset)
    src.set('length',s_length)
    src.text=source
    return ET.tostring(event, pretty_print=True,with_tail=False, xml_declaration=False)
poster_offset=[]

#Finding the index of the poster in the document
def find_poster(offset):
    poster_offset.append(offset)
    tmp_poster_offset=sorted(poster_offset)
    ind_of_poster=tmp_poster_offset[tmp_poster_offset.index(offset)-1]
    return ind_of_poster



def list_ind(of_array,trigger_offset):
    min=1000 #input is list of offsets for the trigger word in original txt file and trigger_offset which is the offset of the one we are looking for
    for index_item in range(len(of_array)):
        if abs(int(of_array[index_item])-int(trigger_offset))<min:
            min=abs(int(of_array[index_item])-int(trigger_offset))
            fin_ind=index_item
    return fin_ind

postrs_id={}
exclude = set(string.punctuation)

#This is to make sure that the tag behind word is completed and is not for previous word
def containsAny(str):
    if '<' in str and '>' in str[-2:]:
        str = ''.join(ch for ch in str if ch not in exclude)
        return str
    else:
        return False
Author_ere={}#keeping the ere id of each author in this list if it exit in the list of author of each txt files
em_poseter_table={}#keeps the m-# for authors and orig_authors in posts and qoutes

def Trigandid(file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file)
    entitiy_id=[]
    root = tree.getroot()
    #postrs_id={} #Storying the value of poster and associated entity id
    for child in root:
        for item in child:
            if "entity" in str(item):
                for atrib in item:
                    for ent_men in atrib:
                        #print ent_men.get('id')
                        entitiy_id.append(str(item.get('id')))
                        entitiy_id.append(str(atrib.get('id')))
                        #entitiy_id.append(atrib.get('id'))# this is added to add all the entities
                        if ent_men.text in myarray:# ent_men should change to actual poster
                            em_poseter_table[str(atrib.get('id'))]=str(ent_men.text)+','+str(atrib.get('offset'))
                            poster_hash[str(atrib.get('offset'))]=ent_men.text###***
                            poster_offset.append(int(atrib.get('offset')))###***#author offset:[14, 943, 5256, 2157, 1014, 5184, 2228]
                            postrs_id[ent_men.text]=item.get('id')#exp:{'Gazpacho': 'ent-30', 'Patrick1000': 'ent-45', 'randman': 'ent-8'}
                            entitiy_id.append(str(item.get('id')))#+" "+str(atrib.get('offset')))
                            Author_ere[ent_men.text]=str(item.get('id'))+" "+str(atrib.get('id'))+" "+str(atrib.get('offset'))+" "+str(atrib.get('length'))


    temp_elemrecord={}
    Array_of_Trigger=[]
    for child in root:
        if child.tag == "relations"or"hopper":
            for item in child.iter('relation_mention'):
                for elm in item:
                    if elm.tag=="trigger":
                        temp_elemrecord['trigger']= elm.text
                        temp_id=item.get('id')
                        temp_elemrecord['Length']=elm.get('length')
                        temp_elemrecord['Offset']=elm.get('offset')
                    if elm.tag!="trigger":
                        if str(elm.get('entity_id')) in str(entitiy_id):#checks to see if that specific author was added to the list before which is only possible if it is in source fille
                            temp_elemrecord['ent_id']=elm.get('entity_id')
                    if len(temp_elemrecord)>3:#this is bigger than three because size of temp_elm if it has the entity id it will be larger than 3 and this is what we are looking for
                        #print temp_elemrecord['trigger'], temp_elemrecord['ent_id']
                        Array_of_Trigger.append(temp_elemrecord['trigger']+" "+temp_elemrecord['ent_id']+" "+temp_elemrecord['Length']+" "+temp_elemrecord['Offset']+" "+temp_id)
                        temp_elemrecord.clear()
                temp_elemrecord.clear()
            for item in child.iter('event_mention'):
                for elm in item:
                    if elm.tag=="trigger":
                        temp_elemrecord['trigger']= elm.text
                        temp_id=item.get('id')
                        temp_elemrecord['Length']=elm.get('length')
                        temp_elemrecord['Offset']=elm.get('offset')
                    if elm.tag!="trigger":
                        if str(elm.get('entity_id')) in str(entitiy_id):
                            temp_elemrecord['ent_id']=elm.get('entity_id')
                    if len(temp_elemrecord)>3:
                        #print temp_elemrecord['trigger'],temp_elemrecord['ent_id']
                        Array_of_Trigger.append(temp_elemrecord['trigger']+" "+temp_elemrecord['ent_id']+" "+temp_elemrecord['Length']+" "+temp_elemrecord['Offset']+" "+temp_id)
                        temp_elemrecord.clear()
                temp_elemrecord.clear()

    return Array_of_Trigger# returns array of events and entity Id


#def find_section(file,entity)

def findingCBtags(file,entityif,keyword):
    filestring=" "
    with open(file,"r") as f:
        for line in f:
            filestring=filestring+" "+line




myarray=[]#list of the poster that we get from the input text files
path = 'temp_source'

import glob
path = 'temp_source/*.txt'
path_ere='tmp_ere/*.xml'
files=glob.glob(path)#list of original text files
xfiles=glob.glob(path_ere)#list of ere files
for xfl in xfiles:
    Author_ere.clear()#This is a hashtable which stroes poster and it's id
    print xfl #printing the xml file address that is being processed
    myarray=Getting_Authors('temp_xml/'+str(xfl[8:-13])+'.cmp.txt.xml') #adding the authors of each text files to the list My array
    finallarray=Trigandid(xfl)
    filestring=""
    str_s=""
   # myadd='data_orig/BT02162016/'+str(xfl[14:-13])+'.cmp.txt.xml'
    with open('temp_xml/'+str(xfl[8:-13])+'.cmp.txt.xml','r') as mytagged: #reading the CB output for the old data xfl [14:13] works
        for line in mytagged:# reading that gain and finding the poster name
            filestring=filestring+" "+line# splitting the content of each poster seperately
        splitar=filestring.split("</post>")
    with open ('temp_source/'+str(xfl[8:-13])+'.cmp.txt','r') as input_data:#
            for line in input_data:
                str_s=str_s+" "+line
    rel_flag=False
    ev_flag=False
    root = ET.Element('committed_belief_doc')
    root.set('id','tree-000000000000000')
    Belief_ano = ET.SubElement(root, 'belief_annotations')
    check=False
    for events in finallarray:
        phrasal_entity_flag=True
        tmp_arra=[]
        event_arr=[]
        if len(events.split())==6:
            tmp_arra.append([events.split()[0]+" "+events.split()[1]])
            tmp_arra.append([events.split()[0]])#this part takes care of multi word events and split them like pass away to pass and away
            tmp_arra.append([events.split()[1]])
        elif len(events.split())==7:
            tmp_arra.append([events.split()[0]+" "+events.split()[1]+" "+events.split()[2]])
            tmp_arra.append([events.split()[0]+" "+events.split()[1]])
            tmp_arra.append([events.split()[1]+" "+events.split()[2]])
            tmp_arra.append([events.split()[0]])#this part takes care of multi word events and split them like pass away to pass and away
            tmp_arra.append([events.split()[1]])
        else:
            tmp_arra.append([events.split()[0]])
        for item in tmp_arra:#tmp_arra contains
             #for name, age in Author_ere.iteritems():
              #      temp_ere=age.split(" ")
                #if temp_ere[0] == item[1]:# it checks the ent id
                try:
                        if len(item[0].split(" "))>1:
                            event_arr=item[0].split(" ")
                        else:
                            event_arr.append(item[0])
                        for tmp_event in event_arr:
                        #ind here should be change to be accurate
                            source_arr=find_ind(str_s,tmp_event)
                            xml_array=find_ind(filestring,tmp_event)

                            final_index=list_ind(source_arr,events.split()[-2])
                            ind=xml_array[final_index]#This filnds the index of the specific event in the tagged file to see if its tagged
                            name=poster_hash[str(find_poster(int(events.split()[-2])))]
                            poster_offset.remove(int(events.split()[-2]))
                            if (phrasal_entity_flag==True)  :
                                    if len(event_arr)>1:#if one of the words were tagged do not look for the next one for example if in blown up either blown or up is tagged just skip to the next word
                                        phrasal_entity_flag=False
                                    check=True
                                    #Printing all the taggs in each file
                                    source=m_id_return(str(xfl[8:-13]),int(events.split()[-2]))
                                    source_id_n_offset=em_poseter_table[source]
                                    source_id=source_id_n_offset.split(',')[0]
                                    offset=source_id_n_offset.split(',')[1]
                                    print (events.split()[-1],item[0],events.split()[-2],events.split()[2],'CB',source_id,offset,str(len(source_id)),str(source))#Sample out put <NA> coming em-791 | admirable m-192 1222 9

                                    if "relm" in events.split()[-1]:
                                        if rel_flag==False:
                                            rltions = ET.SubElement(Belief_ano, 'relations')
                                            rel_flag=True
                                        creat_xml_relat(events.split()[-1],item[0],events.split()[-2],events.split()[2],'CB',source_id,offset,str(len(source_id)),str(source))
                                    if "em" in events.split()[-1]:
                                        if ev_flag==False:
                                            evnts = ET.SubElement(Belief_ano, 'events')
                                            ev_flag=True
                                        creat_xml_event(events.split()[-1],item[0],events.split()[-2],events.split()[2],'CB',source_id,offset,str(len(source_id)),str(source))
                except:
                    pass


    if check:
        output_file = open( 'tmp_out/'+str(xfl[8:-13])+'.best.xml', 'w' )
        output_file.write( '<?xml version="1.0"?>\n')
        output_file.write(ET.tostring(root, pretty_print=True,with_tail=True, xml_declaration=False))
        output_file.close()
        poster_hash.clear()
        em_poseter_table.clear()
        poster_offset=[]

