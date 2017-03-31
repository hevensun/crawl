var casper = require('casper').create();
var utils  = require('utils');

casper.options.waitTimeout = 1000;

url = casper.cli.get('url');
casper.start(url);
//casper.thenOpen('http://h5.m.taobao.com/awp/core/detail.htm?id=10314043465', function() {
casper.then(function() {
        //this.echo(this.getTitle());
        var html = this.getPageContent();
        html = html.replace(/\r/ig, "");
        html = html.replace(/\n/ig, "");

        this.echo("content:" + html);
        //require('fs').write("out.txt", url + "" + html+"\n", 'w');
        });

casper.run();

