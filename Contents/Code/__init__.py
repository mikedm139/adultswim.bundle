VIDEO_PREFIX	=	"/video/adultswim"
NAME          	=	L('Title')

FEED_URL		= 	"http://video.adultswim.com/adultswimdynamic/asfix-svc/episodeSearch/getAllEpisodes?sortByEpisodeRanking=DESC&categoryName=&filterByEpisodeType=PRE,EPI&filterByCollectionId=&filterByAuthType=true&networkName=AS"
EPISODE_LIST	= 	"http://video.adultswim.com/adultswimdynamic/asfix-svc/episodeSearch/getAllEpisodes?sortByDate=DESC&filterByEpisodeType=PRE,EPI&filterByCollectionId=%s&filterByAuthType=true&networkName=AS" #limit=0&offset=0&

ART             =	"art-default.jpg"
ICON	       	=	"icon-default.png"

####################################################################################################
def Start():
	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, '[adult swim]', ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

	ObjectContainer.art        = R(ART)
	ObjectContainer.title1     = NAME
	DirectoryObject.thumb      = R(ICON)

####################################################################################################
def VideoMainMenu():
	oc = ObjectContainer()
	data = XML.ElementFromURL(FEED_URL)
	show_ids = []
	for episode in data.xpath('//episode'):
		showId = episode.get('showId')
		showName = episode.get('collectionTitle')
		if showId in show_ids:
			continue
		else:
			oc.add(DirectoryObject(key=callback(ShowMenu, showName=showName, showId=showId), title=shownName))
			show_ids.append(showId)
	oc.objects.sort(key = lambda obj: obj.title)
	return oc

####################################################################################################
def ShowMenu(showName, showId):
	oc = ObjectContainer(title2=showName)
	ep_list = XML.ElementFromURL(EPISODE_LIST % showId)
	for episode in ep_list.xpath('//episode'):
		title = episode.get('title')
		show = episode.get('collectionTitle')
		epIndex = episode.get('subEpisodeNumber')
		season = episode.get('epiSeasonNumber')
		try:
		    epIndex = int(epIndex)
		    absIndex = None
		except:
		    epIndex = episode.get('episodeNumber')
		    epIndex = int(epIndex.partition(season)[2])
		season = int(season)
		summary = episode.xpath('./description')[0].text
		thumb = episode.get('thumbnailUrl')
		content_rating = episode.get('rating')
		duration = episode.get('duration')
		try:
		    duration = int(duration)
		except:
		    duration = None
		date = episode.get('originalPremiereDate')
		try:
		    date = Datetime.ParseDate(date)
		except:
		    date = None
		episodeUrl = episode.xpath('./episoeLink')[0].get('episodeUrl')
		oc.add(EpisodeObject(url=episodeUrl, title=title, show=show, index=epIndex, season=season, summary=summary,
			content_rating=content_rating, duration=duration, thumb=Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)))
	return oc