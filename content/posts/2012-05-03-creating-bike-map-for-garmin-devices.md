+++
title = "Creating a bike map for Garmin devices based on OSM data"
date = 2012-05-03T20:44:00+00:00
lastmod = 2013-10-09T21:14:41.771000+00:00
url = "/2012/05/creating-bike-map-for-garmin-devices.html"
slug = "creating-bike-map-for-garmin-devices"
tags = ["OpenStreetMap", "navigation", "maps", "tutorial", "GPS", "Garmin"]
+++

<table align="center" cellpadding="0" cellspacing="0" class="tr-caption-container" style="margin-left: auto; margin-right: auto; text-align: center;"><tbody>
<tr><td style="text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjie3bVzMtasmO6iC5XS88UWjjCKplZ1_XTgRCcu65R6casWSTdT5ZicGSt7rquj6Yd01NB7k86usr36zzOzt9ETFxGSwKAOyymdFsySRKhrn-_9vHwl4jxpql5BudAuLJpdOIL-MPzjx8/s1600/Task+Switching_2012-05-03_16-30-09.png" imageanchor="1" style="margin-left: auto; margin-right: auto;"><img border="0" height="305" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjie3bVzMtasmO6iC5XS88UWjjCKplZ1_XTgRCcu65R6casWSTdT5ZicGSt7rquj6Yd01NB7k86usr36zzOzt9ETFxGSwKAOyymdFsySRKhrn-_9vHwl4jxpql5BudAuLJpdOIL-MPzjx8/s400/Task+Switching_2012-05-03_16-30-09.png" width="400" /></a></td></tr>
<tr><td class="tr-caption" style="text-align: center;">The end result: a cycle map in Basecamp</td></tr>
</tbody></table>
<small><i>Update September 2012:</i> A while ago, Henning suggested minor modifications to the commands in steps 2 and 6 that should improve performance.</small><br />
<br />
I don't think I've written a plug for OpenStreetMap (OSM) on this blog yet, but in case you didn't know: OSM is an awesome project, and I'm a regular contributor to and user of their database.<br />
<br />
In preparation for my ride to Toronto I wanted to create a bike map to put on my <a href="http://www.amazon.com/gp/product/B00542NVS2/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=B00542NVS2&amp;linkCode=as2&amp;tag=riorpi-20">Garmin GPS</a>. For many regions in Europe pre-made cycling maps for Garmin are available but you have to DIY. I had created a OSM-based cycling map before but it only covered an area of 200km around Montreal. Creating that map had not been without problems, and unfortunately in the meantime I forgot a lot of the steps necessary. Consequently, this time I'm going to document the process for myself and others. I've tried to keep the instructions as dummy-friendly as possible, not requiring any deep understanding of the processes and programs involved. Feel free to ask questions in the comments and I'll try to answer them. <br />
<br />
Before we get started, I should send out props to OSM-contributor and bike tourer <a href="http://www.aighes.de/OSM/index.php">Henning Scholland/aighes</a>. If you live in Europe you don't have to create your owns maps but just download the ones he created. He has also been very helpful in guiding me through the process of generating my first map. Now let's make a map.<br />
<h2>







Step 1: Download data</h2>
First you have to download the data of the desired region. In the ideal case somebody will already have prepared an extract for that region. If that's the case you can move to step 3. In Canada, however, it is  tricky: on the one hand, you probably won't want a map of <i>all</i> Canada (I heard Canada is big and cycling in the Northern Territories is kinda lonesome); on the other hand you probably want to include some parts of the US. In order to achieve that you will have to create your own extract, either from the "<a href="http://wiki.openstreetmap.org/wiki/Planet.osm#Worldwide_data">planet</a>," i.e. the entirety of all OSM data, or from the <a href="http://download.geofabrik.de/">North America extract</a> which has a more manageable download size of about 5GB.<br />
<br />
<h2>







Step 2: Determine the bounding box and extract data</h2>
Once you have downloaded the several gigabytes of data you will use the tool osmosis to extract the chunk of data that you want. That chunk is called the "bounding box", and it is basically a rectangle, defined by the coordinates of its four corners.&nbsp; <br />
<br />
Install and run <a href="http://wiki.openstreetmap.org/wiki/Osmosis">Osmosis</a>: Download Osmosis and extract it into a folder. Open the command line and navigate to that folder. Run Osmosis as follows: <br />
<br />
<code>osmosis --read-pbf file="c:\Users\Harald\Downloads\america_north.osm.pbf" --bounding-box left=-81.0131836 top=47.2195681 right=-69.8730469 bottom=42.5368920 cascadingRelations --write-pbf file=Northeast.osm</code><br />
<br />
The <code>read-pbf</code> option tells osmosis what kind of input file it is dealing with. The <code>file</code> parameter is the map data file you downloaded in step 1. The easiest way for entering the correct&nbsp; <code>bounding box</code> values is by using the 
export function on the openstreetmap.org slippy map: zoom to the desired area, click 
"Export," and copy the four coordinates you need (if you don't
 have quite the bounding box you want you can click "Select area 
manually" and then draw a rectangle). What <code>cascadingRelations</code> does I don't really know but it's probably good to include it. <code>write-xml </code>determines the output format and shouldn't be changed. The final <code>file</code> then determines where to the output will be written.<br />
<br />
Extracting the bounding box for a large region can take a while and create big files (in my case it was 8GB for an area of 520 by 880 km).<br />
<h2>

Step 3: Split the tiles</h2>
For reasons that don't need to concern you the bounding box extract will now have to be split up into tiles before the actual map making begins. For that download the tool <a href="http://www.mkgmap.org.uk/page/tile-splitter">splitter</a> and extract it to a folder.&nbsp; Install and run splitter with the following parameters:<br />
<br />
<code>C:\Users\Harald\Desktop\splitter-r200\java -Xmx1500m -jar splitter.jar c:\Users\Harald\Desktop\osmosis-0.40.1\bin\Northeast.osm</code><br />
<br />
Depending on how big your extract is and how much memory your machine has you will have to adjust the memory allocation with the <code>Xmx</code> parameter. Stated simply: you want to allocate as much memory as possible. If you try to allocate too much you'll get an error message and can adjust the value down. My system has 4GB RAM and I couldn't assign 2000M but 1500M worked. If you don't have enough memory assigned the splitting process will fail. Once again, the splitting will take a while (in my case about 10 minutes). The end result will be a whole bunch of .pbf files, a file called template.args, and one file called areas.list.<br />
<h2>

Step 4: Download boundaries</h2>
In order to have a functioning address search on your Garmin, you will need to integrate administrative boundaries while making the map (i.e. the boundaries of countries, states/provinces, municipalities). Download the file from <a href="http://www.navmaps.eu/index.php/developers/bound">here</a> and unzip into the same directory as your tiles. (Please note that searching for addresses doesn't work all that well in Canada because of a lack of boundary data.)<br />
<h2>

Step 5: Download map style</h2>
If you want to use the style of the aighes's RadReiseKarte (bike touring map), download <code><a href="http://www.aighes.de/OSM/data/style.zip">style.zip</a></code> from his homepage and extract the contents of the <code>data</code> directory into the folder containing your map data. You should now install <a href="http://wiki.openstreetmap.org/wiki/Mkgmap#Download">mkgmap</a>. After the installation you can do a quick test of the style file: run mkgmap as follows (depending on where you put your files you have to modify the path to the style folder):<br />
<br />
<code>java -jar mkgmap.jar --style-file=data/style_rrk --
list-styles</code><br />
<br />
This should produce an output of<br />
<code>The following styles are available:<br />style_rrk&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1: No summary available</code><br />
<br />
<h2>
Step 6: Create the map with mkgmap</h2>
Now run the following, very long command from the directory containing your map data and the style directory:<br />
<br />
<code>java -Xmx1500m -jar mkgmap.jar --max-jobs=4 --read-config=data\style_rrk\options --code-page=1252 --mapname=66000000 --overview-mapname=66000000 --family-name="Cyclemap Northeast" --series-name="Cyclemap Northeast April 2012" --description="Cyclemap April 2012" --family-id=6600 --output-dir=maps\&nbsp;</code><code> </code><br />
<br />
Unless you know what you're doing (I certainly didn't when I was doing this myself) I don't recommend changing anything except for the series name and family name parameters and the path to the desired output directory. Once again, you'll have to wait a while until mkgmap finishes. 
<br />
<h2>

Step 7: Install map into Mapsource/Basecamp</h2>
Mkgmap can create IMG files which you can copy directly onto your Garmin device. In general, however, it's easier to install the map in Mapsource/Basecamp first. This requires you to download the <a href="http://nsis.sourceforge.net/Download">NSIS installation system</a>. Start the program, select the output-dir defined in the previous step, and voila: you have an installer for your new map.<br />
<br />
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-g4OvM8B2qNIknlWS8v4BUMY-FHFbmVfE2J10fGyG5DPHPcH2oIoemyBZoZkOaM43_tLYZRmK9cBszPT_-wCR58rv-GGxMgERuDC9dxPCoYiFR9aEPDPvK-s35ov2ZZFCxmcLIWrC4gA/s1600/Garmin+BaseCamp_2012-05-03_16-31-18.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="243" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-g4OvM8B2qNIknlWS8v4BUMY-FHFbmVfE2J10fGyG5DPHPcH2oIoemyBZoZkOaM43_tLYZRmK9cBszPT_-wCR58rv-GGxMgERuDC9dxPCoYiFR9aEPDPvK-s35ov2ZZFCxmcLIWrC4gA/s400/Garmin+BaseCamp_2012-05-03_16-31-18.png" width="400" /></a></div>
<br />
This is what the map will look like in Basecamp at a higher zoom level (I couldn't get a good pic of the map on my Garmin Etrex).
