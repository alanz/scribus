# -*- coding: utf-8 -*-

""" This is a simple 'Calendar creation wizard' for Scribus. It's a fully
rewritten Calendar.py from Scribus examples. Enjoy.

DESCRIPTION & USAGE:
This script needs Tkinter. It will create a GUI with available options
for easy calendar page creation. You'll get new pages with calendar
tables into a new document you are asked for. Position of the
objects in page is calculated with the "golden-ratio" aspect from the
page margins.

Steps to create:
    1) Fill requested values in the Calendar dialog
    2) You will be prompted for new document
    3) You will be prompted for new paragraph style which will be used
       in calendar text frames. It could be changed later.

There are 2 types of calendar supported:
    1) Classic calendar with one month matrix per page. I suggest
       here PORTRAIT orientation.
    2) Horizontal event calendar with one week per page with huge place
       for human inputs. There should be LANDSCAPE imho.
    3) Horizontal event calendar with one week per page with huge place
       for human inputs. There should be LANDSCAPE imho.

But everything works with both orientations well of course too.

AUTHORS:
    Petr Vanek <petr@scribus.info>
    Bernhard Reiter <ockham@raz.or.at>

LICENSE:
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""

import sys
import calendar
import datetime

try:
    from scribus import *
except ImportError:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

try:
    # I wish PyQt installed everywhere :-/
    from Tkinter import *
    from tkFont import Font
except ImportError:
    print "This script requires Python's Tkinter properly installed."
    messageBox('Script failed',
               'This script requires Python\'s Tkinter properly installed.',
               ICON_CRITICAL)
    sys.exit(1)


localization = {
'Catalan' :
    [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
      'Juny', 'Juliol', 'Agost', 'Setembre',
      'Octubre', 'Novembre', 'Desembre'],
     ['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte', 'Diumenge']],
'Catalan-short' :
    [['Gener', 'Febrer', 'Març', 'Abril', 'Maig',
      'Juny', 'Juliol', 'Agost', 'Setembre',
      'Octubre', 'Novembre', 'Desembre'],
     ['Dl', 'Dm', 'Dc', 'Dj', 'Dv', 'Ds', 'Dg']],
# Catalan by "Cesc Morata" <atarom@gmail.com>
'Czech' :
    [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
        'Červen', 'Červenec', 'Srpen', 'Září',
        'Říjen', 'Listopad', 'Prosinec'],
     ['Pondělí','Úterý','Středa','Čtvrtek','Pátek','Sobota', 'Neděle']],
'Czech-short' :
    [['Leden', 'Únor', 'Březen', 'Duben', 'Květen',
        'Červen', 'Červenec', 'Srpen', 'Září',
        'Říjen', 'Listopad', 'Prosinec'],
     ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']],
# Croatian by daweed
'Croatian' :
    [['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj',
        'Lipanj', 'Srpanj', 'Kolovoz', 'Rujan',
        'Listopad', 'Studeni', 'Prosinac'],
     ['Ponedjeljak','Utorak','Srijeda','Četvrtak','Petak','Subota', 'Nedjelja']],

'Dutch' :
    [['Januari', 'Februari', 'Maart', 'April',
      'Mei', 'Juni', 'Juli', 'Augustus', 'September',
      'Oktober', 'November', 'December'],
     ['Maandag','Dinsdag','Woensdag','Donderdag','Vrijdag','Zaterdag', 'Zondag']],
# Dutch by "Christoph Schäfer" <christoph-schaefer@gmx.de>
'English' :
    [['January', 'February', 'March', 'April',
      'May', 'June', 'July', 'August', 'September',
      'October', 'November', 'December'],
     ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']],
'English-short' :
    [['January', 'February', 'March', 'April', 'May',
      'June', 'July', 'August', 'September', 'October',
      'November', 'December'],
     ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']],
'Finnish' :
    [['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu',
      'Toukokuu', 'Kesäkuu', 'Heinäkuu', 'Elokuu', 'Syyskuu',
      'Lokakuu', 'Marraskuu', 'Joulukuu'],
     ['ma','ti','ke','to','pe','la', 'su']],
'French':
    [['Janvier', u'F\xe9vrier', 'Mars', 'Avril',
      'Mai', 'Juin', 'Juillet', u'Ao\xfbt', 'Septembre',
      'Octobre', 'Novembre', u'D\xe9cembre'],
     ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']],
'German' :
    [['Januar', 'Februar', u'M\xe4rz', 'April',
      'Mai', 'Juni', 'Juli', 'August', 'September',
      'Oktober', 'November', 'Dezember'],
     ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']],
'German (Austrian)' :
    [[u'J\xe4nner', 'Feber', u'M\xe4rz', 'April',
      'Mai', 'Juni', 'Juli', 'August', 'September',
      'Oktober', 'November', 'Dezember'],
     ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']],
# Hungarian by Gergely Szalay szalayg@gmail.com	      
'Hungarian' :
    [['Január', 'Február', 'Március', 'Április',
       'Május', 'Június', 'Július', 'Augusztus', 'Szeptember',
       'Október', 'November', 'December'],
    ['Hétfő','Kedd','Szerda','Csütörtök','Péntek','Szombat','Vasárnap']],
'Italian' :
    [['Gennaio', 'Febbraio', 'Marzo', 'Aprile',
       'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
       'Ottobre', 'Novembre', 'Dicembre'],
    [u'Luned\xec', u'Marted\xec', u'Mercoled\xec', u'Gioved\xec', u'Venerd\xec', 'Sabato', 'Domenica']],
# Norwegian by Joacim Thomassen joacim@net.homelinux.org
'Norwegian' :
    [['Januar', 'Februar','Mars', 'April','Mai', 'Juni','Juli', 'August','September', 'Oktober', 'November', 'Desember'],
     ['Mandag', 'Tirsdag','Onsdag', 'Torsdag','Fredag', 'Lørdag','Søndag']],
# Polish by "Łukasz [DeeJay1] Jernaś" <deejay1@nsj.srem.pl>
'Polish' :
    [['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj',
      'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
      'Październik', 'Listopad', 'Grudzień'],
     ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']],
'Portuguese' :
    [['Janeiro', 'Fevereiro', u'Mar\xe7o', 'Abril',
      'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
      'Outubro', 'Novembro', 'Dezembro'],
     ['Segunda-feira', u'Ter\xe7a-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', u'S\xe1bado', 'Domingo']],
# Romanian by Costin Stroie <costinstroie@eridu.eu.org>
'Romanian' :
    [['Ianuarie', 'Februarie', 'Martie', 'Aprilie',
      'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie',
      'Octombrie', 'Noiembrie', 'Decembrie'],
     ['Luni','Mar\xc8\x9bi','Miercuri','Joi','Vineri','S\xc3\xa2mb\xc4\x83t\xc4\x83', 'Duminic\xc4\x83']],
'Russian' :
    [['Январь', 'Февраль', 'Март', 'Апрель',
      'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
      'Октябрь', 'Ноябрь', 'Декабрь'],
     ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота', 'Воскресенье']],
'Slovak' :
    [['Január', 'Február', 'Marec', 'Apríl',
      'Máj', 'Jún', 'Júl', 'August', 'September',
      'Október', 'November', 'December'],
      ['Pondelok','Utorok','Streda','Štvrtok','Piatok','Sobota', 'Nedeľa']],
'Slovak-short' :
    [['Január', 'Február', 'Marec', 'Apríl',
      'Máj', 'Jún', 'Júl', 'August', 'September',
      'Október', 'November', 'December'],
      ['Po','Ut','St','Št','Pi','So', 'Ne']],
'Spanish' :
    [['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
      'Junio', 'Julio', 'Agosto', 'Septiembre',
      'Octubre', 'Noviembre', 'Diciembre'],
     ['Lunes', 'Martes', u'Mi\xe9rcoles', 'Jueves', 'Viernes', u'S\xe1bado', 'Domingo']],
'Swedish' :
    [['Januari', 'Februari','Mars', 'April','Maj', 'Juni','Juli', 'Augusti','September', 'Oktober', 'November', 'December'],
     ['Måndag', 'Tisdag','Onsdag', 'Torsdag','Fredag', 'Lördag','Söndag']]
}


from math import sqrt

class ScCalendar:
    """ Parent class for all calendar types """

    def __init__(self, year, months=[], firstDay=calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        """ Setup basic things """
        # params
        self.drawSauce = drawSauce # draw supplementary image?
        self.wholePage = wholePage # Do not leave space for an image
        self.year = year
        self.months = months
        self.lang = lang
        # day order
        self.dayOrder = localization[self.lang][1]
        if firstDay == calendar.SUNDAY:
            self.firstDaySun = True
            dl = self.dayOrder[:6]
            dl.insert(0, self.dayOrder[6])
            self.dayOrder = dl
        else:
            self.firstDaySun = False
        self.mycal = calendar.Calendar(firstDay)
        self.layerImg = 'Calendar image'
        self.layerCal = 'Calendar'
        self.pStyleDate = "Date" # paragraph styles
        self.pStyleWeekday = "Weekday"
        self.pStyleYear = "Year"
        self.pStyleMonth = "Month"
        self.pStyleWeekNo = "WeekNo"
        self.pStyleMiniCal = "MiniCal"
        self.masterPage = "CalendarBackground"
        self.masterPageImage = "Image"
        self.sepMonths = sepMonths
        # settings
        self.firstPage = True # create only 2nd 3rd ... pages. No 1st one.
        calendar.setfirstweekday(firstDay)
        progressTotal(len(months))

    def setupDocVariables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        page = getPageSize()
        self.pagex = page[0]
        self.pagey = page[1]
        marg = getPageMargins()
        # See http://docs.scribus.net/index.php?lang=en&page=scripterapi-page#-getPageMargins
        self.margint = marg[0]
        self.marginl = marg[1]
        self.marginr = marg[2]
        self.marginb = marg[3]
        self.width = self.pagex - self.marginl - self.marginr
        self.height = self.pagey - self.margint - self.marginb

    def goldenMean(self, aSize):
        """ Taken from samples/golden-mean.py."""
        return aSize * ((sqrt(5) - 1)/2)

    def applyTextToFrame(self, aText, aFrame):
        """ Insert the text with style. """
        setText(aText, aFrame)
        setStyle(self.pStyleDate, aFrame)

    def createCalendar(self):
        """ Walk through months dict and call monthly sheet """
        if not newDocDialog():
            return 'Create a new document first, please'
        createParagraphStyle(name=self.pStyleDate, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.pStyleWeekday, alignment=ALIGN_CENTERED)
#        createParagraphStyle(name=self.pStyleWeekday, alignment=ALIGN_RIGHT) # original alignment
        createParagraphStyle(name=self.pStyleYear)
        createParagraphStyle(name=self.pStyleMonth)
        createParagraphStyle(name=self.pStyleWeekNo, alignment=ALIGN_RIGHT)
        createParagraphStyle(name=self.pStyleMiniCal, alignment=ALIGN_CENTERED)
        originalUnit = getUnit()
        setUnit(UNIT_POINTS)
        self.setupDocVariables()
        if self.drawSauce or self.wholePage:
            createLayer(self.layerImg)
        createLayer(self.layerCal)
        self.setupMasterPage()
        run = 0
        for i in self.months:
            run += 1
            progressSet(run)
            cal = self.mycal.monthdatescalendar(self.year, i + 1)
            self.createMonthCalendar(i, cal)
        setUnit(originalUnit)
        return None

    def createLayout(self):
        """ Create the page and optional bells and whistles around """
        if self.wholePage and self.drawSauce:
            self.createImagePage()
            setActiveLayer(self.layerImg)
            createImage(self.marginl, self.margint, self.width, self.height)
        self.createPage()
        if self.drawSauce:
            setActiveLayer(self.layerImg)
            self.createImage()
        setActiveLayer(self.layerCal)

    def createPage(self):
        """ Wrapper to the new page with layers """
        if self.firstPage:
            self.firstPage = False
            newPage(-1, self.masterPage) # create a new page using the masterPage
            deletePage(1) # now it's safe to delete the first page
            gotoPage(1)
            return
        newPage(-1, self.masterPage)

    def createImagePage(self):
        """ Wrapper to the new page with layers """
        if self.firstPage:
            self.firstPage = False
            newPage(-1, self.masterPageImage) # create a new page using the masterPage
            deletePage(1) # now it's safe to delete the first page
            gotoPage(1)
            return
        newPage(-1, self.masterPageImage)

class ScEventCalendar(ScCalendar):
    """ Parent class for event
        (horizontal event, vertical event) calendar types """

    def __init__(self, year, months = [], firstDay = calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        ScCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)

    def printMonth(self, cal, month, week):
	    """ Print the month name(s) """
	    if week[6].day < 7:
		    if (week == cal[len(cal)-1]):
			    self.createHeader(localization[self.lang][0][month] + self.sepMonths + localization[self.lang][0][(month+1)%12])
		    elif ((month-1) not in self.months):
			    self.createHeader(localization[self.lang][0][(month-1)%12] + self.sepMonths + localization[self.lang][0][month])
	    else:
		    self.createHeader(localization[self.lang][0][month])

    def createMonthCalendar(self, month, cal):
        """ Draw one week calendar per page """
        for week in cal:
            # Avoid duplicate week around the turn of the months:
            # Only include week:
            # * If it's not the first week in a month, or, if it is:
            # * If it starts on the first weekday
            # * If the month before it isn't included
            if (week != cal[0]) or (week[0].day == 1) or ((month-1) not in self.months):
				self.createLayout()
				self.printMonth(cal, month, week)
				self.printWeekNo(week)

				for day in week:
				    self.printDay(day)

class ScHorizontalEventCalendar(ScEventCalendar):
    """ One day = one row calendar. I suggest LANDSCAPE orientation.\
        One week per page."""

    def __init__(self, year, months = [], firstDay = calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        ScEventCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)

    def setupDocVariables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        # golden mean
        ScCalendar.setupDocVariables(self)
        self.gmean = self.width - self.goldenMean(self.width) + self.marginl
        # calendar size = gmean
        # rows and cols
        self.rowSize = self.height / 8

    def printWeekNo(self, week):
        """ Dummy for now
            (for this type of calendar - see ScVerticalEventCalendar) """
        return

    def printDay(self, j):
        """ Print a given day """
        cel = createText(self.gmean + self.marginl,
                         self.margint + (1 + (j.weekday()-calendar.firstweekday())%7) * self.rowSize,
                         self.width - self.gmean, self.rowSize)
        setText(str(j.day), cel)
        setStyle(self.pStyleDate, cel)

    def createHeader(self, monthName):
        """ Draw calendar header: Month name """
        cel = createText(self.gmean + self.marginl, self.margint,
                            self.width - self.gmean, self.rowSize)
        setText(monthName, cel)
        setStyle(self.pStyleMonth, cel)

    def createImage(self):
        """ Wrapper for everytime-the-same image frame. """
        if self.drawSauce:
            createImage(self.marginl, self.margint, self.gmean, self.height)

    def setupMasterPage(self):
        """ Create a master page (not used for this type of calendar """
        createMasterPage(self.masterPage)
        closeMasterPage()

class ScVerticalCalendar(ScCalendar):
    """ Parent class for vertical
        (classic, vertical event) calendar types """

    def __init__(self, year, months = [], firstDay = calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        ScCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)

    def setupDocVariables(self):
        """ Compute base metrics here. Page layout is bordered by margins and
        virtually divided by golden mean 'cut' in the bottom. The calendar is
        in the bottom part - top is occupied with empty image frame. """
        # gloden mean
        ScCalendar.setupDocVariables(self)
        if self.wholePage:
            self.gmean = self.height
        else:
            self.gmean = self.height - self.goldenMean(self.height) + self.margint
        # calendar size
        self.calHeight = self.height - self.gmean + self.margint
        # rows and cols
        if self.wholePage:
            self.rowSize = self.gmean / 7
        else:
            self.rowSize = self.gmean / 8
        self.colSize = self.width / 7
        if self.wholePage:
            self.miniCalPriorX = self.marginl+4.8*self.colSize
            self.miniCalPriorY = self.margint
            self.miniCalNextX = self.marginl+6.0*self.colSize
            self.miniCalNextY = self.margint
            self.miniCalWidth = self.colSize
            self.miniCalHeight = self.rowSize*1.45

    def setupMasterPage(self):
        """ Draw invariant calendar header: Days of the week """
        if self.wholePage:
            createMasterPage(self.masterPageImage)
            closeMasterPage()
        createMasterPage(self.masterPage)
        editMasterPage(self.masterPage)
        setActiveLayer(self.layerCal)
        if self.wholePage:
            vd = self.colSize / 8.0
            rs = self.rowSize * 1.5
            rh = self.rowSize * 0.5
        else:
            vd = 0
            rs = self.rowSize
            rh = self.rowSize
        colCnt = 0
        for j in self.dayOrder: # days
            cel = createText(self.marginl + colCnt*self.colSize,
                             self.calHeight + rs,
                             self.colSize, rh)
            setLineColor("Black", cel)  # comment this out if you do not want border to cells
            setTextDistances(0,0,vd,0,cel)
            setText(j, cel)
            setStyle(self.pStyleWeekday, cel)
            if ((self.wholePage and self.firstDaySun       and colCnt == 0) or
                (self.wholePage and (not self.firstDaySun) and colCnt == 6)):
              setFillColor("Red", cel)
              setFillShade(10, cel)
            colCnt+=1
        if self.wholePage:
            # header = createText(self.marginl+6*self.colSize, self.calHeight, self.colSize, self.rowSize)
            header = createText(self.marginl+0*self.colSize, self.calHeight, self.colSize, 1.5*self.rowSize)
            setText(str(self.year), header)
            setStyle(self.pStyleYear, header)
            setFillColor("Red", header)
            setFillShade(10, header)
            vd = self.colSize / 5.5
            setTextDistances(0,0,vd,0,header)

            # minical bounding boxes
            self.createMiniCalBox(self.miniCalPriorX,self.miniCalPriorY,self.miniCalWidth,self.miniCalHeight)
            self.createMiniCalBox(self.miniCalNextX ,self.miniCalNextY ,self.miniCalWidth,self.miniCalHeight)

            cal = self.mycal.monthdatescalendar(self.year, 3)
            rowCnt = 2
            for week in cal:
                colCnt = 0
                for day in week:
                    cel = createText(self.marginl + colCnt * self.colSize,
                                     self.calHeight + rowCnt * self.rowSize,
                                     self.colSize, self.rowSize)

                    setLineColor("Black", cel)  # comment this out if you do not want border to cells
                    if ((self.wholePage and self.firstDaySun       and colCnt == 0) or
                        (self.wholePage and (not self.firstDaySun) and colCnt == 6)):
                      setFillColor("Red", cel)
                      setFillShade(10, cel)
                    colCnt += 1
                    # if day.month == month + 1:
                    #                         setText(str(day.day), cel)
                    #                         setStyle(self.pStyleDate, cel)
                rowCnt += 1

# setTextDistances(...)
# setTextDistances(left, right, top, bottom, ["name"])

# Sets the text distances of the text frame "name" to the values "left" "right",
# "top" and "bottom". If "name" is not given the currently selected item is
# used.

# May throw ValueError if any of the distances are out of bounds (must be positive).

        closeMasterPage()

    def createMiniCalBox(self,x,y,w,h):
        """ Draw a shaded background for the mini calendars"""
        header = createText(x,y,w,h)
        setFillColor("Black", header)
        setFillShade(10, header)

    def createHeader(self, monthName):
        """ Draw calendar header: Month name """
        if self.wholePage:
            header = createText(self.marginl + 1.0 * self.colSize, self.calHeight, 2.0*self.colSize, self.rowSize)
            vd = self.colSize / 5.5
            # header = createText(self.marginl, self.calHeight, self.width, self.rowSize)
        else:
            header = createText(self.marginl, self.calHeight, self.width, self.rowSize)
            vd = 0
        setText(monthName, header)
        setStyle(self.pStyleMonth, header)
        setTextDistances(0,0,vd,0,header)

    def createImage(self):
        """ Wrapper for everytime-the-same image frame. """
        if self.drawSauce:
            createImage(self.marginl, self.margint,
                        self.width, self.calHeight - self.margint)

class ScClassicCalendar(ScVerticalCalendar):
    """ Calendar matrix creator itself. I suggest PORTRAIT orientation.
        One month per page."""

    def __init__(self, year, months = [], firstDay = calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        ScVerticalCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)

    def createMonthCalendar(self, month, cal):
        """ Create a page and draw one month calendar on it """
        self.createLayout()
        self.createHeader(localization[self.lang][0][month])
        if self.wholePage:
            if month == 0:
                priorMonth = 11
                priorYear = self.year-1
                priorCal = self.mycal.monthdatescalendar(self.year-1, 12)
                nextMonth = 1
                nextYear = self.year
                nextCal  = self.mycal.monthdatescalendar(self.year, 2)
            elif month == 11:
                priorMonth = 10
                priorYear = self.year
                priorCal = self.mycal.monthdatescalendar(self.year, month)
                nextMonth = 0
                nextYear = self.year + 1
                nextCal  = self.mycal.monthdatescalendar(self.year+1, 1)
            else:
                priorMonth = month - 1
                priorYear = self.year
                priorCal = self.mycal.monthdatescalendar(self.year, month)
                nextMonth = month + 1
                nextYear = self.year
                nextCal  = self.mycal.monthdatescalendar(self.year, month+2)
            self.createMiniCalendar(priorMonth,priorYear,priorCal
                                    ,self.miniCalPriorX,self.miniCalPriorY,self.miniCalWidth,self.miniCalHeight)
            self.createMiniCalendar(nextMonth,nextYear,nextCal
                                    ,self.miniCalNextX,self.miniCalNextY,self.miniCalWidth,self.miniCalHeight)
        rowCnt = 2
        for week in cal:
            colCnt = 0
            for day in week:
                if self.wholePage:
                    hd = self.rowSize / 16.0
                    vd = self.colSize / 20.0
                else:
                    hd = 0
                    vd = 0
                cel = createText(self.marginl + colCnt * self.colSize,
                                 self.calHeight + rowCnt * self.rowSize,
                                 self.colSize, self.rowSize)

                setTextDistances(0,hd,vd,0,cel)
		#setLineColor("Black", cel)  # comment this out if you do not want border to cells
                colCnt += 1
                if day.month == month + 1:
					setText(str(day.day), cel)
					setStyle(self.pStyleDate, cel)
            rowCnt += 1

    def createMiniCalendar(self, month, year, cal,x,y,w,h):
        """ Create a mini one month calendar on """
        #self.createHeader(localization[self.lang][0][month])
        colWidth = w / 7
        rowHeight = h / 8
        # colWidth = w
        # rowHeight = h
        header = createText(x, y, w, rowHeight)
        setText(localization[self.lang][0][month] + " " + str(year), header)
        setStyle(self.pStyleMiniCal, header)

        # Add day legend
        if self.firstDaySun:
            days = ["S","M","T","W","T","F","S"]
        else:
            days = ["M","T","W","T","F","S","S"]
        rowCnt = 1
        for day in range(7):
            cel = createText(x + day * colWidth,
                             y + rowCnt * rowHeight,
                             colWidth, rowHeight)
            setText(days[day], cel)
            setStyle(self.pStyleDate, cel)

        rowCnt = 2
        for week in cal:
            colCnt = 0
            for day in week:
                cel = createText(x + colCnt * colWidth,
                                 y + rowCnt * rowHeight,
                                 colWidth, rowHeight)

		#setLineColor("Black", cel)  # comment this out if you do not want border to cells
                colCnt += 1
                if day.month == month + 1:
					setText(str(day.day), cel)
					setStyle(self.pStyleMiniCal, cel)
            rowCnt += 1

class ScVerticalEventCalendar(ScVerticalCalendar, ScEventCalendar):
    """ One day = one column calendar. I suggest LANDSCAPE orientation.\
        One week per page."""

    def __init__(self, year, months = [], firstDay = calendar.SUNDAY, drawSauce=True, wholePage=False, sepMonths='/', lang='English'):
        ScVerticalCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)
        ScEventCalendar.__init__(self, year, months, firstDay, drawSauce, wholePage, sepMonths, lang)

    def printDay(self, j):
        """ Print a given day """
        cel = createText(self.marginl + ((j.weekday()-calendar.firstweekday())%7)*self.colSize,
                         self.calHeight + self.rowSize,
                         self.colSize/5, self.rowSize)
        setText(str(j.day), cel)
        setStyle(self.pStyleDate, cel)

    def printWeekNo(self, week):
        """ Print the week number for the given week"""
        weekCel = createText(self.marginl, self.calHeight, self.width, self.rowSize)
        # Week number: of this week's Thursday.
        # See http://docs.python.org/library/datetime.html#datetime.date.isocalendar
        # Note that week calculation isn't perfectly universal yet:
        # http://en.wikipedia.org/wiki/Week_number#Week_number
        setText(str(week[(calendar.THURSDAY-calendar.firstweekday())%7].isocalendar()[1]), weekCel)
        setStyle(self.pStyleWeekNo, weekCel)

class TkCalendar(Frame):
    """ GUI interface for Scribus calendar wizard.
        It's ugly and very simple. I can say I hate Tkinter :-/"""

    def __init__(self, master=None):
        """ Setup the dialog """
        # reference to the localization dictionary
        self.key = 'English'
        Frame.__init__(self, master)
        self.grid()
        self.master.resizable(0, 0)
        self.master.title('Scribus Calendar Wizard')
        #define widgets
        self.statusVar = StringVar()
        self.statusLabel = Label(self, textvariable=self.statusVar)
        self.statusVar.set('Select Options and Values')
        # langs
        # change the height = to match number of langs.
        self.langLabel = Label(self, text='Select language:')

        self.langFrame = Frame(self)
        self.langFrame.grid()
        self.langScrollbar = Scrollbar(self.langFrame, orient=VERTICAL)
        self.langScrollbar.grid(row=0, column=1, sticky=N+S)
        self.langListbox = Listbox(self.langFrame, selectmode=SINGLE, height=10, yscrollcommand=self.langScrollbar.set)
        self.langListbox.grid(row=0, column=0, sticky=N+S+E+W)
        self.langScrollbar.config(command=self.langListbox.yview)

        keys = localization.keys()
        keys.sort()
        for i in keys:
            self.langListbox.insert(END, i)
        self.langButton = Button(self, text='Change language', command=self.languageChange)
        # calendar type
        self.typeLabel = Label(self, text='Calendar type')
        self.typeVar = IntVar()
        self.typeClRadio = Radiobutton(self, text='Classic', variable=self.typeVar, value=0)
        self.typeEvRadio = Radiobutton(self, text='Event (Horizontal)', variable=self.typeVar, value=1)
        self.typeVERadio = Radiobutton(self, text='Event (Vertical)', variable=self.typeVar, value=2)
        # start of week
        self.weekStartsLabel = Label(self, text='Week begins with:')
        self.weekVar = IntVar()
        self.weekMondayRadio = Radiobutton(self, text='Mon', variable=self.weekVar, value=calendar.MONDAY)
        self.weekSundayRadio = Radiobutton(self, text='Sun', variable=self.weekVar, value=calendar.SUNDAY)
        # year
        self.yearLabel = Label(self, text='Year:')
        self.yearVar = StringVar()
        self.yearEntry = Entry(self, textvariable=self.yearVar, width=4)
        self.wholeYearLabel = Label(self, text='Whole year:')
        self.wholeYear = IntVar()
        self.wholeYearCheck = Checkbutton(self, command=self.setWholeYear, variable=self.wholeYear)
        # months
        self.monthLabel = Label(self, text='Months:')
        self.monthListbox = Listbox(self, selectmode=MULTIPLE, height=12)
        # layout stuff
        self.imageLabel = Label(self, text='Draw Image Frame:')
        self.imageVar = IntVar()
        self.imageCheck = Checkbutton(self, variable=self.imageVar)
        # whole page?
        self.wpLabel = Label(self, text='Use whole page (landscape):')
        self.wpVar = IntVar()
        self.wpCheck = Checkbutton(self, variable=self.wpVar)
        # Months separator
        self.sepMonthsLabel = Label(self, text='Months separator:')
        self.sepMonthsVar = StringVar()
        self.sepMonthsEntry = Entry(self, textvariable=self.sepMonthsVar, width=4)
        # closing/running
        self.okButton = Button(self, text="OK", width=6, command=self.okButonn_pressed)
        self.cancelButton = Button(self, text="Cancel", command=self.quit)
        # setup values
        self.weekMondayRadio.select()
        self.typeClRadio.select()
        self.yearVar.set(str(datetime.date(1, 1, 1).today().year + 1))
        self.sepMonthsVar.set('/')
        self.imageCheck.select()
        #self.wpCheck.select()
        # make layout
        self.columnconfigure(0, pad=6)
        currRow = 0
        self.statusLabel.grid(column=0, row=currRow, columnspan=4)
        currRow += 1
        self.langLabel.grid(column=0, row=currRow, sticky=W)
        self.monthLabel.grid(column=3, row=currRow, sticky=W)
        currRow += 1
        self.langFrame.grid(column=0, row=currRow, rowspan=7, sticky=N)
        self.typeLabel.grid(column=1, row=currRow, sticky=E)
        self.typeClRadio.grid(column=2, row=currRow, sticky=W)
        self.monthListbox.grid(column=3, row=currRow, rowspan=9)
        currRow += 1
        self.typeEvRadio.grid(column=2, row=currRow, sticky=W)
        currRow += 1
        self.typeVERadio.grid(column=2, row=currRow, sticky=W)
        currRow += 1
        self.weekStartsLabel.grid(column=1, row=currRow, sticky=N+E)
        self.weekMondayRadio.grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.weekSundayRadio.grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.yearLabel.grid(column=1, row=currRow, sticky=N+E)
        self.yearEntry.grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.wholeYearLabel.grid(column=1, row=currRow, sticky=N+E)
        self.wholeYearCheck.grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.imageLabel.grid(column=1, row=currRow, sticky=N+E)
        self.imageCheck.grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.wpLabel.   grid(column=1, row=currRow, sticky=N+E)
        self.wpCheck.   grid(column=2, row=currRow, sticky=N+W)
        currRow += 1
        self.langButton.grid(column=0, row=currRow)
        currRow += 1
        self.sepMonthsLabel.grid(column=1, row=currRow, sticky=N+E)
        self.sepMonthsEntry.grid(column=2, row=currRow, sticky=N+W)
        currRow += 3
        self.rowconfigure(currRow, pad=6)
        self.okButton.grid(column=1, row=currRow, sticky=E)
        self.cancelButton.grid(column=2, row=currRow, sticky=W)
        # fill the values
        self.realLangChange()

    def languageChange(self, lang='English'):
        """ Called by Change button. Get language list value and
            call real re-filling. """
        ix = self.langListbox.curselection()
        if len(ix)==0:
            self.statusVar.set('Select a language, please')
            return
        self.realLangChange(lang=self.langListbox.get(ix[0]))

    def realLangChange(self, lang='English'):
        """ Real widget setup. Ot takes values from localization dictionary.
        [0] = months, [1] Days """
        self.key = lang
        self.monthListbox.delete(0, END)
        self.wholeYear.set(0)
        for i in localization[lang][0]:
            self.monthListbox.insert(END, i)

    def setWholeYear(self):
        """ All/none months selection. It's called after "Whole year" check button
        click. """
        if self.wholeYear.get() == 1:
            self.monthListbox.selection_set(0, END)
        else:
            self.monthListbox.selection_clear(0, END)

    def okButonn_pressed(self):
        """ User variables testing and preparing """
        # year
        try:
            year = self.yearVar.get().strip()
            if len(year) != 4:
                raise ValueError
            year = int(year, 10)
        except ValueError:
            self.statusVar.set('Year must be in the "YYYY" format e.g. 2005.')
            return
        # months
        selMonths = self.monthListbox.curselection()
        if len(selMonths) == 0:
            self.statusVar.set('At least one month must be selected.')
            return
        months = []
        for i in selMonths:
            months.append(int(i))
        # draw images etc.
        if self.imageVar.get() == 0:
            draw = False
        else:
            draw = True
        # Skip image and use whole page?
        if self.wpVar.get() == 0:
            wholePage = False
        else:
            wholePage = True
        # create calendar (finally)
        if self.typeVar.get() == 0:
            cal = ScClassicCalendar(year, months, self.weekVar.get(), draw, wholePage, self.sepMonthsVar.get(), self.key)
        elif self.typeVar.get() == 1:
            cal = ScHorizontalEventCalendar(year, months, self.weekVar.get(), draw, wholePage, self.sepMonthsVar.get(), self.key)
        else:
            cal = ScVerticalEventCalendar(year, months, self.weekVar.get(), draw, wholePage, self.sepMonthsVar.get(), self.key)
        self.master.withdraw()
        err = cal.createCalendar()
        if err != None:
            self.master.deiconify()
            self.statusVar.set(err)
        else:
            self.quit()

    def quit(self):
        self.master.destroy()


def main():
    """ Application/Dialog loop with Scribus sauce around """
    try:
        statusMessage('Running script...')
        progressReset()
        root = Tk()
        app = TkCalendar(root)
        root.mainloop()
    finally:
        if haveDoc() > 0:
            redrawAll()
        statusMessage('Done.')
        progressReset()

if __name__ == '__main__':
    main()

