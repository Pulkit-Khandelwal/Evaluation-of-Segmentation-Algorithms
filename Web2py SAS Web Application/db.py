db = DAL('sqlite://storage.sqlite')


## db for user Data
#from PIL import Image
#from Images import RESIZE
db.define_table('dataset',
    Field('name',requires=IS_NOT_EMPTY(),unique=True),
    Field('description','text',requires=IS_NOT_EMPTY()))

#PK. The field thumb has been added to create the thumbnails
db.define_table('uploads',
    Field('dataset', 'reference dataset'),
    Field('filename', represent = lambda x, row: "None" if x == None else 
x[:45]),
    Field('image', 'upload', uploadseparate=True, requires=IS_NOT_EMPTY() and IS_IMAGE(extensions=('jpeg', 'png','jpg','tif')) ),
    Field('thumb', 'upload', uploadseparate=True, requires=IS_NOT_EMPTY() and IS_IMAGE(extensions=('jpeg', 'png', 'jpg', 'tif')),writable=False,readable=False))



## db for user information
db.define_table('person',
    Field('name'),
    Field('married', 'boolean'),
    Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
    Field('age','integer',default=30),
    Field('Methodology',requires=IS_IN_SET(['Seed Points', 'Strokes'])))

db.person.name.requires = IS_NOT_EMPTY()
db.person.age.requires=IS_INT_IN_RANGE(0,120)


## db for experiment
db.define_table('experiment',
    Field('expName',unique=True),
    Field('briefing', 'boolean',default=False),
    Field('BriText','text',default='This is the briefing'),
    Field('ConText','text',default='This is the consent'),
    Field('instruction', 'boolean',default=False),
    Field('InsText','text',default='This is the instruction'),
    Field('practice', 'boolean',default=False),
    Field('praDataset','string'),
    Field('praImageNumber','integer',default=0,requires=IS_NOT_EMPTY()),
    Field('expDataset', 'string'),
    Field('expImageNumber','integer',default=1,requires=IS_NOT_EMPTY()),
    Field('result', 'boolean',default=False),
    Field('survey', 'boolean',default=False),
    Field('link','text',default='http://www.google.ca'),
    Field('debriefing', 'boolean',default=False),
    Field('DeText','text',default='This is the debriefing'),
    format='%(name)s')
    
db.experiment.expDataset.requires = IS_IN_DB(db,'dataset.name','%(name)s',zero=T('none'))
db.experiment.praDataset.requires = IS_IN_DB(db,'dataset.name','%(name)s',zero=T('none'))
db.experiment.praImageNumber.requires=IS_INT_IN_RANGE(0,999)
db.experiment.expImageNumber.requires=IS_INT_IN_RANGE(1,999)

#PK. db for participant information
db.define_table('person_experiment_relation',
    Field('personID','integer'),
    Field('experimentD','string'),
    Field('practiceD','string'),
    Field('expID','integer'))

db.person_experiment_relation.practiceD.requires = IS_IN_DB(db,'praDataset.id','%(name)s',zero=T('none'))
db.person_experiment_relation.experimentD.requires = IS_IN_DB(db,'expDataset.id','%(name)s',zero=T('none'))
db.person_experiment_relation.personID.requires = IS_IN_DB(db,'person.id','%(name)s',zero=T('none'))
db.person_experiment_relation.expID.requires = IS_IN_DB(db,'experiment.id','%(name)s',zero=T('none'))


#PK. Table for the result of each experiment. Each entry is an Image
db.define_table('trialsresult',
    Field('imagesID','integer'),
    Field('imagesFilename','string'),
    Field('expID','integer'),
    Field('personID','string'),
    Field('experimentD','integer'),
    Field('timeLapse','integer'),
    Field('DATA','string',uploadseparate=True))

db.trialsresult.imagesID.requires = IS_NOT_EMPTY()
db.trialsresult.imagesFilename.requires = IS_NOT_EMPTY()
db.trialsresult.expID.requires = IS_IN_DB(db,'experiment.id','%(name)s',zero=T('none'))
db.trialsresult.personID.requires = IS_IN_DB(db,'person.id','%(name)s',zero=T('none'))
db.trialsresult.experimentD.requires = IS_IN_DB(db,'expDataset.id','%(name)s',zero=T('none'))
db.trialsresult.timeLapse.requires = IS_NOT_EMPTY()
db.trialsresult.DATA.requires = IS_NOT_EMPTY()
