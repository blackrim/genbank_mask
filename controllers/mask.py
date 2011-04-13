import datetime

"""
some basic functionality for mask
"""

def index():
	return dict()

def batch_enter_mask():
	reason_options = [OPTION(cat.type,_value=cat.id) for cat in db().select(db.reason.ALL)]
	form = FORM(TABLE(TR('genbank ids (gi\'s):',TEXTAREA(_name='gis',value='enter genbank gi numbers (one on each line)')),
	TR('reason:',SELECT(*reason_options,**dict(_name="reason_category"))),
	TR('comment (for all, optional):',INPUT(_name='comment')),
        TR('',INPUT(_type='submit',_value='submit'), _action=URL('batch_enter_mask')),))
	if form.accepts(request.vars, session):
		response.flash = 'form accepted'
		gis = request.vars['gis']
		if gis == 'enter genbank gi numbers (one on each line)':
			response.flash = "you didn't enter anything"
			return dict(form=form)
		try:
			giss = gis.split()
			rid = request.vars['reason_category']
			for i in giss:
				if len(i) < 4: # should be longer than this
					continue
				gin = db.mask.insert(genbank_id = i,date_added=datetime.datetime.now(),reason=rid)
				if len(request.vars['comment']) > 0:
					db.mask_comment.insert(mask_id = gin,comment=request.vars['comment'],date_added=datetime.datetime.now())
			response.flash = "inserted " +str(len(giss))+ " records"
		except:
			response.flash = "There was an error. Try again or email the list to stephen_a_smith@brown.edu"
	elif form.errors:
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'
	return dict(form=form)

def enter_mask():
	reason_options = [OPTION(cat.type,_value=cat.id) for cat in db().select(db.reason.ALL)]
	form = FORM(TABLE(TR('genbank id (gi):',INPUT(_name='gis')),
	TR('reason:',SELECT(*reason_options,**dict(_name="reason_category"))),
	TR('comment (for all, optional):',INPUT(_name='comment')),
        TR('',INPUT(_type='submit',_value='submit'), _action=URL('batch_enter_mask')),))
	if form.accepts(request.vars, session):
		response.flash = 'form accepted'
		if gis == 'enter genbank gi numbers (one on each line)':
			response.flash = "you didn't enter anything"
			return dict(form=form)
		try:
			giss = request.vars['gis']
			rid = request.vars['reason_category']
			gin = db.mask.insert(genbank_id = giss,date_added=datetime.datetime.now(),reason=rid)
			if len(request.vars['comment']) > 0:
				db.mask_comment.insert(mask_id = gin,comment=request.vars['comment'],date_added=datetime.datetime.now())
			response.flash = "inserted " +str(len(giss))+ " records"
		except:
			response.flash = "There was an error. Try again or email the list to stephen_a_smith@brown.edu"
	elif form.errors:
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'
	return dict(form=form)

def view_mask():
	return dict()

def query_mask():
	try:
		gid = request.vars['id']
		res = db(db.mask.genbank_id == gid).select(db.mask.ALL)
		for i in res:
			reason = i['reason']
			comments = i['mask_comment'].select(db.mask_comment.ALL)
			for j in comments:
				print j
	except:
		response.flash = "please enter a genbank id"
	return dict()

def dump_mask():
	res = db().select(db.mask.genbank_id)
	return res

def enter_reason():
	form = FORM(TABLE(
	TR('reason (be thoughtful):',INPUT(_name='reason')),
	TR('description:',TEXTAREA(_name='descr',value='')),
        TR('',INPUT(_type='submit',_value='submit'), _action=URL('enter_reason')),)) 
	if form.accepts(request.vars, session):
		reason = request.vars['reason']
		descr = request.vars['descr']
		try:
			db.reason.insert(type = reason,description=descr)
			response.flash = "inserted reason"
		except:
			response.flash = "error inserting reason"
	elif form.errors:
		response.flash = "form has errors"
	else:
		response.flash = "please fill out the form"
	return dict(form=form)
