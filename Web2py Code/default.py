# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## - index is the main page to choose the experimenter or user
## - enterDemographics is the page to ask user to input their information
## - instruction is the page to show the instructions
## - practice is the page for users to practice to work on the system
## - pResult is the page to give users their practice results
## - experiment is the page to do the real practice
## - expResult is the page to give users their experiment results
## - questionnaire is the page to ask users to fill out the questionnaires experimenters need
## - last is the page to tell users they have complete all the tasks they need to do
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
def index():
    redirect(URL('experimenter'))
    return dict()


def informedConsent():
    exp = session.exp
    Briefing = exp.BriText
    Consent = exp.ConText
    form = FORM(TABLE(TR(INPUT(_name='agree',_type='checkbox',value=False),
    T('I agree to the terms and conditions'),''),
    TR('','',INPUT(_type='submit',_value='Continue'))))
    if form.process().accepted:
        if form.vars.agree:
            redirect(URL('enterDemographics'))
        else:
            response.flash = 'you must agree the consent to continue'
    return dict(form=form,Briefing=Briefing,Consent=Consent)

# PK. A new form1 has been added. It takes the input from the participant in the form of User ID. Also, refer to the function exisitinguser()

def enterDemographics():
    exp = session.exp

    """
    page to ask for the user's name and may some other info as well
    """

    form1 = FORM(
           TR('User id:',
              INPUT(_type='integer',_name='user_id',requires=IS_NOT_EMPTY()),INPUT(_type='submit',_value='SUBMIT')),keepvalues =True)

    if form1.accepts(request.vars,keepvalues=True):

        redirect(URL('existinguser',vars=dict(user_id=form1.vars.user_id)))
    gis = request.vars.user_id
    record = db.person(gis)
    form = SQLFORM(db.person,record)


    if form.process().accepted:
            row = db(db.person.id == form.vars.id).select().first()
            session.personID = row.id
            session.practiceD = exp.praDataset
            session.experimentD = exp.expDataset
            
            db.person_experiment_relation.insert(personID=session.personID,expID=session.expID,practiceD=session.practiceD,experimentD=session.experimentD)
            if exp.instruction:
                redirect(URL(instruction))
            elif exp.practice:
                redirect(URL(practice))
            else:
                redirect(URL(experiment))


    return dict(form=form,form1=form1,record=record)

# PK. This is the page where the user gets directed when he/she chooses to use an existing User ID. Also, refer to the function enterDemographics()

def existinguser():
    """
    page for exisiting use selection

    """

    exp = session.exp
    gis = request.vars.user_id
    record = db.person(gis)
    form = SQLFORM(db.person,record)

    if form.process().accepted:
            row = db(db.person.id == form.vars.id).select().first()
            session.personID = row.id
            session.practiceD = exp.praDataset
            session.experimentD = exp.expDataset

            db.person_experiment_relation.insert(personID=session.personID,expID=session.expID,practiceD=session.practiceD,experimentD=session.experimentD)
            if exp.instruction:
                redirect(URL(instruction))
            elif exp.practice:
                redirect(URL(practice))
            else:
                redirect(URL(experiment))

    return dict(form=form)
     

def instruction():
    """
    page to show the instructions or may vedios to the users
    """
    exp=session.exp
    PDS=exp.practice
    instruction=exp.InsText

    return dict(PDS=PDS,instruction=instruction)

#PK. The following page opens up everytime a user wants (from any page) to access the Instructions

def instro():
    """
    page to show the instructions or may vedios to the users
    """
    exp=session.exp
    instruction=exp.InsText

    return dict(instruction=instruction)
    
    
# PK. Changes were made in the following function so that a proper count of the images in a particular experiment is recorded properly.
# This helped in solving the problem of improper navigation through the various images.
# Changed dataset.name to dataset.id
# if session.images == None:
# was specified before the
# images = db(db.uploads.dataset == dataset.id).select(orderby='<random>')
# This should not be the case as it defaults to one image only and does not load the next image on hitting Enter

def practice():
    """
    page for user to practice

    """
    exp = session.exp
    Max = exp.praImageNumber

    dataset = db(db.dataset.id==exp.praDataset,ignore_common_filters=True).select().first()

    images = db(db.uploads.dataset == dataset.id).select(orderby='<random>')
    session.images = images

    session.num += 1

    if session.log == None:
        session.log = []

    PR=exp.result
    return dict(PR=PR,images=session.images,i=session.num,Max=Max)

#PK. If a participant wants to practice on new images, the he/she gets redirected to another set of images on the following page.
def yo():
   
    exp = session.exp
    Max = exp.praImageNumber
    #changed below to .id
    dataset = db(db.dataset.id==exp.praDataset,ignore_common_filters=True).select().first()

    #if session.images == None:
    images = db(db.uploads.dataset == dataset.id).select(orderby='<random>')
    session.images = images

    session.number += 1


    if session.log == None:
        session.log = []


    PR=exp.result
    return dict(PR=PR,images=session.images,i=session.number,Max=Max)


#PK. Unable to display the practice and experiment results due to some customization of the download function
import os
def pResult():
    exp = session.exp


    PTS=exp.survey
    DE=exp.debriefing

    return dict(PTS=PTS,DE=DE)

# PK. Changes were made in the following function so that a proper count of the images in a particular experiment is recorded properly.
# This helped in solving the problem of improper navigation through the various images.
# Changed dataset.name to dataset.id
# if session.images == None:
# was specified before the
# images = db(db.uploads.dataset == dataset.id).select(orderby='<random>')
# This should not be the case as it defaults to one image only and does not load the next image on hitting Enter


def experiment():
    """
    page for the actual experiments

    """
    exp = session.exp
    Max = exp.expImageNumber

    dataset = db(db.dataset.id==exp.expDataset,ignore_common_filters=True).select().first()


    images = db(db.uploads.dataset == dataset.id).select(orderby='<random>')

    session.images = images

    session.counter += 1

    if session.log == None:
        session.log = []

    
    ER=exp.result
    PTS=exp.survey
    DE=exp.debriefing


    
    return dict(ER=ER,PTS=PTS,DE=DE,images=session.images,i=session.counter,Max=Max)

#PK. trialsresult is the Database Table inserted here
# Different attributes from JSON String can be seen here

def newImage():
    exp = session.exp
    import gluon.contrib.simplejson as sj
    from skimage import io
    import numpy as np
    import os, string, datetime
    from PIL import Image, ImageDraw
    from subprocess import Popen, PIPE, STDOUT

    json = request.body.read()
    data = sj.loads(json) #data is an object
    session.log.append(data)
    img = os.path.basename(data["image"])
    filename = os.path.basename(data["filename"])
    no_ext = os.path.splitext(filename)[0]
    filename = string.join([no_ext, "tif"], ".")


    # Load the test image
    subdir = img.split('.')[2][:2]
    path = os.path.join(request.folder, "uploads", "uploads.image", subdir)
    private = os.path.join(request.folder, "private")
    im = Image.open(os.path.join(path, img))

    greyscale = np.zeros(im.size[::-1], dtype=np.uint8)

    colours = {"#00ff00": 128, "#0000ff": 255}
    #Ignore this part. Was playing around with ImageDraw initially
    #yo = Image.new('RGBA', (400, 400), (0, 255, 0))
    #draw = ImageDraw.Draw(yo)
    #draw.line((0, 0, yo.size[0], yo.size[1]), fill=255, width=3)



    # Reconstruct the input strokes in a grayscale with label 1 meaning background, label 2 meaning foreground.
    # NOTE: This does NOT reconstruct the strokes correctly.  Need to draw lines in between
    # the successive points.
    for evt in data["events"]:
        if not evt["erased"]:
            intensity = colours[evt["colour"]]
            for pt in evt["points"]:
                greyscale[pt["y"]][pt["x"]] = intensity


    # Get the Person ID for the current session
    PID = session.personID
    if PID == None:
        session.subdir = (session.subdir or 1) -1
        PID = session.subdir

    # Create an output folder for the current person and session based on the current date (if no such folder exists)
    now = datetime.datetime.now().date()
    subdir = string.join([str(PID), str(now)], "_")
    resultfolder = os.path.join(private, "output", subdir)
    if not os.path.exists(resultfolder):

       os.makedirs(resultfolder)

    # Save the stroke image for use by the segmentation algorithm.
    gsimg = filename + ".strokes.tif"
    gsfile = os.path.join(resultfolder, gsimg)
    io.imsave(gsfile, greyscale)

    # Execute the external segmentation algorithm.
    testdir = os.path.join(private, "SegmentEpiUniform", "testimages")
    script = os.path.join(testdir, "run.sh")
    p = Popen([script, filename, gsfile, resultfolder], cwd=testdir)
    p.wait()

    # No idea what this does or why it's here. - MGE
    session.script = string.join([script, filename, gsfile, subdir], " ")


    timelapse = data["elapsed"]


    db.trialsresult.insert(imagesID=session.images[0],imagesFilename=filename,personID=session.personID,expID=session.expID,experimentD=session.experimentD,timeLapse=timelapse,DATA=data)

    return 0



#PK. Unable to display the practice and experiment results due to some customization of the download function
def expResult():
    """
    page to show user's experimental result and ground truth
    """

    exp = session.exp

    PTS=exp.survey
    DE=exp.debriefing
    
    return dict(PTS=PTS,DE=DE)

def questionnaire():
    """
    page for the questionnaire
    """

    exp = session.exp
    DE=exp.debriefing
    
    return dict(DE=DE)

def last():
    import gluon.contrib.simplejson as sj
    import os, string, datetime, json
    """
    page to say bye bye to users
    """
    PID = session.personID
    if PID == None:
        session.subdir = (session.subdir or 1) -1
        PID = session.subdir

    now = datetime.datetime.now().date()
    subdir = string.join([str(PID), str(now)], "_")
    outfile = string.join([subdir, "log"], ".")
    output = os.path.join(request.folder, "private", "output", subdir)
    outputfile = os.path.join(output, outfile)
    
    if not os.path.exists(output):
        os.makedirs(output)

    logs = {"logs": session.log}
    with open(outputfile, 'wt') as out:
        res = json.dump(logs, out, sort_keys=False, indent=4, separators=(',', ': '))
    return dict(message1="All tasks have been completed!", message2="Thanks for your cooperation and have a nice day!")

def experimenter():
    """
    page for experimenter
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    return dict()

## list datasets.
def MDS():
    """
    page to manage data set
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]

    ## all rows of datasets
    rows = db(db.dataset.id>0).select(db.dataset.ALL)
    return dict(rows=rows)


def ME():
    """
    page to manage experiment
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    session.counter = -1
    session.num = -1
    session.number = -1
    session.images = None
    session.personID = None
    session.log = None
    ## all rows of experiments
    rows = db(db.experiment.id>0).select(db.experiment.ALL)
    return dict(rows=rows)

def MWE():
    """
    page to manage workflow
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    return dict()

def imageEdit():
    """
    page to edit images
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    images = db().select(db.uploads.ALL, orderby=db.uploads.dataset)
    return dict(images=images)
    
def DSimageEdit():
    """
    page to edit images
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    record = None
    record = db(db.dataset.id == request.args[0],ignore_common_filters=True).select().first()

    rowId = None
    rowId = request.args[0]
    images = db(db.uploads.dataset==record.id).select()



    return dict(images=images,record=record,rowId=rowId)


#PK. Edited the following code for the dispaly of thumbnails.
# Whenever an experimenter uploads a new image in  any dataset, the thimbnail also gets created and can be seen in db.thumb
# The variable dataofimages stores the images in the current dataset and creates thumbnail for each image in that particular dataset.
# Also, refer the function makeThumbnail

def insertImage():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]

    record = None
    record = db(db.dataset.id == request.args[0],ignore_common_filters=True).select().first()

    form = FORM(LABEL(""), INPUT(_name='up_files', _type='file', 
_multiple=True, requires=IS_NOT_EMPTY()),INPUT(_type='submit')) 
# The multiple param lets us choose multiple files.
    if form.process().accepted:
#onvalidation checks the uploaded files to make sure they are only txt, config, or log.
        response.flash = 'files uploaded'


        files = request.vars['up_files'] 
        if not isinstance(files, list): 
        #convert files to a list if they are not one already.
            files = [files]
        for file in files:         
            db.uploads.insert(dataset=record.id, filename=file.filename, image=db.uploads.image.store(file, file.filename))
                        #store is a FIELD method that let's you save a file to disk.  you can choose the directory if you want using the 'path' param.
    else:
       response.flash = 'Choose the Files you would like to upload'

    dataofimages = db(db.uploads.dataset == record.id).select()
    for entry in dataofimages:
        makeThumbnail(db.uploads,entry,size=(40,40))
    return dict(form=form, record=record)

def createDataset():
    """
    page to create new data set
    """
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    form = SQLFORM(db.dataset)
    if form.process().accepted:
        response.flash = 'New data Set created'
        redirect(URL('MDS'))
    return dict(form=form)

def link():
    """
    page to link to the aimed webpage
    """
    exp = session.exp
    redirect(exp.link)
    return dict()

def debriefing():
    exp = session.exp
    Debriefing = exp.DeText
    form = FORM(TABLE(TR(INPUT(_name='agree',_type='checkbox',value=False),
    T('I have been appropriately debriefed about the experiment and all of my question have been answered.'),''),
    TR('','',INPUT(_type='submit',_value='Finish'))))
    if form.process().accepted:
        if form.vars.agree:
            redirect(URL('last'))
        else:
            response.flash = 'If you get any questions, please ask the experimenter, otherwise please agree to continue'

    return dict(form=form,Debriefing=Debriefing)


def createExperiment():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    form = FORM(TABLE(TR(T('Please give a name for this experiment:'),INPUT(_name='name',_type='text',value='Please give a fashion name...')),
        TR(T('Briefing and Consent'),T('include?'),INPUT(_name='Consent_include',_type='checkbox',value=False)),
        TR(T('Partcipant Instrcutions'),T('include?'),INPUT(_name='Instruction_include',_type='checkbox',value=False)),
        TR(T('Practice Data Set'),T('include?'),INPUT(_name='Practice_include',_type='checkbox',value=False)),
        T('Trial Data Set'),
        TR(T('Experiment Result'),T('include?'),INPUT(_name='Result_include',_type='checkbox',value=False)),
        TR(T('Post trial survey'),T('include?'),INPUT(_name='Survey_include',_type='checkbox',value=False)),
        TR(T('Debriefing'),T('include?'),INPUT(_name='Debriefing_include',_type='checkbox',value=False)),
        INPUT(_type='submit',_value='Create')))
    
    exp = None
    
    if form.process().accepted:
        response.flash = 'New experiment start to create'
        
        expID = db.experiment.insert(expName = form.vars.name,
            briefing = form.vars.Consent_include,
            instruction = form.vars.Instruction_include,
            practice = form.vars.Practice_include,
            result = form.vars.Result_include,
            survey = form.vars.Survey_include,
            debriefing = form.vars.Debriefing_include,
            BriText = '',
            ConText = '',
            InsText = '',
            DeText = '')
          
        exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
        session.exp = exp
        session.expID = expID
        if exp.briefing:
            redirect(URL('InputConsent'))
        elif exp.instruction:
            redirect(URL('InputInstruction'))
        elif exp.practice:
            redirect(URL('ChoosePractice'))
        else:
            redirect(URL('ChooseDataSet'))
        
    return dict(form=form,exp=exp)
    
    
def InputConsent():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    
    form = FORM(TABLE(T('Participant Briefing:*'),
        INPUT(_name='PB',_type='text',value='Enter the participant briefing...'),
        T('Participant Consent Form:*'),
        INPUT(_name='PCF',_type='text',value='Enter the participant consent form...'),
        INPUT(_type='submit',_value='Create')))
        
    if form.process().accepted:
        response.flash = 'Briefing and Consent form successfully created.'
        exp.update_record(BriText = form.vars.PB)
        exp.update_record(ConText = form.vars.PCF)
        
        if exp.instruction:
            redirect(URL('InputInstruction'))
        elif exp.practice:
            redirect(URL('ChoosePractice'))
        else:
            redirect(URL('ChooseDataSet'))

    return dict(form=form)    
    
def InputInstruction():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    
    form = FORM(TABLE(T('Participant Instructions:*'),
        INPUT(_name='PI',_type='text',value='Enter the participant instructions ...'),
        INPUT(_type='submit',_value='Create')))
    if form.process().accepted:
        response.flash = 'Participant Instruction successfully created.'
        exp.update_record(InsText = form.vars.PI)
        
        if exp.practice:
            redirect(URL('ChoosePractice'))
        else:
            redirect(URL('ChooseDataSet'))
    return dict(form=form)    
      
    
def ChoosePractice():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    rows = db(db.dataset.id>0).select(db.dataset.ALL)
    #changed below to .id
    form = SQLFORM.factory(Field('dataset',requires=IS_EMPTY_OR(IS_IN_DB(db,'dataset.id','%(name)s',zero=T('choose one')))),
    Field('number','integer',default='number of images used',requires=IS_EMPTY_OR(IS_INT_IN_RANGE(1,1000))),
    buttons = [TAG.button('Create',_type="submit"), TAG.button('Cancel',_type="button",_onClick = "parent.location='%s' " %URL(r=request,f='cancelExp'))])
    if form.process().accepted:
        response.flash = 'Practice Data set successfully selected.'
        exp.update_record(praDataset = form.vars.dataset)
        exp.update_record(praImageNumber = form.vars.number)
        redirect(URL(ChooseDataSet))
    return dict(rows=rows,form=form)  
    
    
def ChooseDataSet():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    
    rows = db(db.dataset.id>0).select(db.dataset.ALL)
     #changed below to .id
    form = SQLFORM.factory(Field('dataset',requires=IS_EMPTY_OR(IS_IN_DB(db,'dataset.id','%(name)s',zero=T('choose one')))),
    Field('number','integer',default='number of images used',requires=IS_EMPTY_OR(IS_INT_IN_RANGE(1,1000))),
    buttons = [TAG.button('Create',_type="submit"), TAG.button('Cancel',_type="button",_onClick = "parent.location='%s' " %URL(r=request,f='cancelExp'))])
        
    if form.process().accepted:
        response.flash = 'Trial Data set successfully selected.'
        exp.update_record(expDataset = form.vars.dataset)
        exp.update_record(expImageNumber = form.vars.number)
        if exp.survey:
            redirect(URL(LinkSurvey))
        elif exp.debriefing:
            redirect(URL(InputDereifing))
        else:
            redirect(URL(ME))
    return dict(rows=rows,form=form) 

def LinkSurvey():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    
    form = FORM(TABLE(T('Participant Post Trial Questionnaire URL:*'),
        INPUT(_name='QU',_type='text',value='http://www.google.ca'),
        INPUT(_type='submit',_value='Add')))
    if form.process().accepted:
        response.flash = 'Questionnaire URL successfully input.'
        exp.update_record(link = form.vars.QU)
        
        if exp.debriefing:
            redirect(URL(InputDereifing))
        else:
            redirect(URL(ME))
    return dict(form=form)  
    
    
def InputDereifing():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    
    expID = session.expID
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    
    form = FORM(TABLE(T('Participant Debriefing Information:*'),
        INPUT(_name='PDI',_type='text',value='Enter the participant debriefing ...'),
        INPUT(_type='submit',_value='Create')))
    if form.process().accepted:
        response.flash = 'Debriefing successfully input.'
        exp.update_record(DeText = form.vars.PDI)
        redirect(URL(ME))
    return dict(form=form)



def editDataset():
    record = None
    record = db(db.dataset.id == request.args[0],ignore_common_filters=True).select().first()
    
    if not record:
        session.flash = T('record does not exist')
        redirect(URL(MDS))
    
    form = SQLFORM(db.dataset, record, deletable=True, delete_label=T('Check to delete'))        
         
    if form.process().accepted:
        session.flash = T('done!')
        redirect(URL(MDS))
    return dict(form=form)
    
def deleteDataset():
    db(db.dataset.id == request.args[0]).delete()
    redirect(URL(MDS))
    return dict(form=form)

def editExperiment():
    session.counter = -1
    session.num = -1
    session.number = -1
    session.images = None
    session.personID = None
    session.log = None
    
    record = None
    record = db(db.experiment.id == request.args[0],ignore_common_filters=True).select().first()
    
    if not record:
        session.flash = T('record does not exist')
        redirect(URL(ME))
    
    form = SQLFORM(db.experiment, record, deletable=True, delete_label=T('Check to delete'),
        buttons=[TAG.button('Back',_type="button",_onClick="parent.location='%s'"%URL(ME)),
        TAG.button('Submit',_type="submit"),A("Run",_class='button',_href=URL('jumpToExp',args=request.args[0]))])
    
         
    if form.process().accepted:
        session.flash = T('done!')
        redirect(URL(ME))
    return dict(form=form)
    
def deleteExperiment():
    db(db.experiment.id == request.args[0]).delete()
    redirect(URL(ME))
    return dict(form=form)
    
def deleteImage():
    db(db.uploads.id == request.args[0]).delete()
    redirect(URL(imageEdit))
    return dict(form=form)

def cancelExp():
    expID = session.expID
    db(db.experiment.id == expID,ignore_common_filters=True).delete()
    redirect(URL('experimenter'))
    return dict(form=form)

def jumpToExp():
    expID = request.args[0]
    exp = db(db.experiment.id == expID,ignore_common_filters=True).select().first()
    session.exp = exp
    session.expID = expID
    
    if exp.briefing:
        redirect(URL('informedConsent'))
    elif exp.instruction:
        redirect(URL(instruction))
    elif exp.practice:
        redirect(URL(practice))
    else:
        redirect(URL(experiment))
    return dict()

#PK. A function to craete thumbnail. Also, refer the function insertImage()

def makeThumbnail(dbtable,ImageID,size=(260,260)):
    try:
        thisImage=db(dbtable.id==ImageID).select()[0]
        from PIL import Image
        import os, uuid
    except: return

    imageName = dbtable.image.retrieve(thisImage.image)[1].name
    im=Image.open(imageName)

    im.thumbnail(size,Image.ANTIALIAS)

    tempThumbSave = request.folder + 'uploads/thumb.jpeg'
    im.save(tempThumbSave, 'jpeg')
    stream = open(tempThumbSave, 'rb')

    thisImage.update_record(thumb=stream)


    return

def show():
    response.menu = [
        (T('Home'),False,URL('default','experimenter')),
        (T('Manage Data Set'),False,URL('default','MDS')),
        (T('Manage Experiment'),False,URL('default','ME')),
        (T('Manage Workflow Element'),False,URL('default','MWE'))
    ]
    address = None
    address = request.args(1)
    image = db.uploads(request.args(0)) or redirect(URL('index'))
    thumb = db.uploads(request.args(0)) or redirect(URL('index'))
    return dict(image=image,address=address,thumb=thumb)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
