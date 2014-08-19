/* Copyright 2012 Aditi Muralidharan. See the file "LICENSE" for the full license governing this code. */Ext.define('WordSeer.store.DocumentStore', {
	extend:'Ext.data.Store',
	model:'WordSeer.model.DocumentModel',
	proxy: {
		type:'ajax',
		noCache: false,
		reader: 'json',
		url: ws_api_path + 'projects/' + project_id + '/documents/',
		extraParams: {
			instance:getInstance(),
	        user:getUsername(),
	        include_text: false,
	    }
	},
})
