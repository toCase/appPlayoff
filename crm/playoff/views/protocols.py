import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.db.models import Q

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm, mm

from reportlab.lib import colors

from PyPDF2 import PdfMerger, PdfReader

from .. import models

pos_participants = []
font_path = os.path.join(settings.STATIC_ROOT, "Roboto-Regular.ttf")
pdfmetrics.registerFont(TTFont('Roboto', font_path))

def draw_net(c, participants):    
    pos_participants.clear()
    width, height = A4    
    count = 0
    if len(participants) == 2:
        count = 2
    elif 2 < len(participants) <= 4:
        count = 4  
    elif 4 < len(participants) <= 8:
        count = 8
    elif 8 < len(participants) <= 16:
        count = 16
    
    #start    
    x = 30
    y = height - 190      
    w = 115
    h = 30
    
    pos_A = []
    for i in range(0, count):
        x1 = x
        y1 = y - i * h  # Отступ вниз для каждого участника
        x2 = x + w
        y2 = y1
        
        c.line(x1, y1, x2, y2)
        pos_A.append((x2, y2))
        
        pos_participants.append((x, y2+5))
        
    drawStage(c, h, w, pos_A, 0)

def drawStage(c, h, w, position:list, stage:int, ):
    new_postion = []
    
    if stage > 0:
        w = 95
    
    for i in range(0, len(position), 2):
        x, y = position[i]
        x2, y2 = position[i + 1]
        c.line(x, y, x2, y2)

        mh = pow(2, stage)                
        y3 = y - (mh * h) / 2
        
        c.line(x, y3, x + w, y3)
        pos_participants.append((x + 5, y3+5))
        
        new_postion.append((x+w, y3))
    new_stage = stage + 1
    if len(new_postion) > 1:
        drawStage(c, h, w, new_postion, new_stage)
        
def drawParticipants(c, participants):
    c.setFont("Roboto", 8)
    
    ps = len(participants)
    if ps == 2 or ps == 4 or ps == 8 or ps == 16:
        for i in range(ps):
            x, y = pos_participants[i]
            c.drawString(x, y, participants[i])
    if ps == 3:
        for i in range(2):
            x, y = pos_participants[i]
            c.drawString(x, y, participants[i])
        x, y = pos_participants[5]
        c.drawString(x, y, participants[2])
    if ps == 5:
        for i in range(2):
            x, y = pos_participants[i]
            c.drawString(x, y, participants[i])
        for i in range(2, ps):
            x, y = pos_participants[i+7]
            c.drawString(x, y, participants[i])
    if ps == 6:
        for i in range(2):
            x, y = pos_participants[i]
            c.drawString(x, y, participants[i])
        x, y = pos_participants[9]
        c.drawString(x, y, participants[2])
        for i in range(3, 5):
            x, y = pos_participants[i+1]
            c.drawString(x, y, participants[i])        
        x, y = pos_participants[11]
        c.drawString(x, y, participants[5])
    if ps == 7:
        for i in range(6):
            x, y = pos_participants[i]
            c.drawString(x, y, participants[i])
        x, y = pos_participants[11]
        c.drawString(x, y, participants[6])

def drawThird(c, participants):
    width, height = A4
    ps = len(participants)
    if ps == 4:
        x, y = pos_participants[3]
        x = 1 * cm + 115 - 40
        y -= 30
    elif 4 < ps <= 8:
        x, y = pos_participants[7]
        x = 1*cm + 115 + 115 - 40
        y -= 30
    elif 8 < ps <= 16:
        x, y = pos_participants[15]
        x = 1*cm + 115 + 115 + 95 - 40
    
    
    # HEADER
    data = [["3-є місце"]]
    table = Table(data, rowHeights=[13], colWidths=[95])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'BOTTOM'),
        ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, x, y)
    
    y -= 60
        
    c.line(x, y, x + 95, y)
    c.line(x, y+30, x + 95, y+30)
    c.line(x+95, y, x+95, y+30)
    c.line(x+95, y+15, x+2*95, y+15)
    
def draw_tab_net(c, participants):
    count = len(participants)
    width, height = A4
    
    x = 30
    y = height - 170  
    
    
    
    if count == 2:
        data = [["ФІНАЛ"]]
    elif 2 < count <= 4:
        data = [["1/2", "ФІНАЛ"]]
    elif 4 < count <= 8:
        data = [["1/4", "1/2", "ФІНАЛ"]]
    elif 8 < count <= 16:
        data = [["1/8", "1/4", "1/2", "ФІНАЛ"]]
    
    col1 = 115
    col2 = 115 
    col3 = 95
    col4 = 95
    
    table = Table(data, rowHeights=[13], colWidths=[col1, col2, col3, col4])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'BOTTOM'),
        ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, x, y)


def create_document(tournament, competition, participants):
    # Создаем холст (Canvas) A4
    buffer = BytesIO()
    # c = canvas.Canvas(f"{competition.idx}.pdf", pagesize=A4)
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Минимальные отступы (5 мм от краев)
    margin = 10 * mm
    
    # Таблица в верхней части
    upper_table_data = [
        ['ОДЕСЬКИЙ ОБЛАСНИЙ ВІДОКРЕМЛЕНИЙ ПІДРОЗДІЛ ГРОМАДСЬКОЇ ОРГАНІЗАЦІЇ\n«ФЕДЕРАЦІЯ ТРАДИЦІЙНОГО КАРАТЕ-ДО УКРАЇНИ»', '', '', '', '', ''],
        ['ПРОТОКОЛ ____', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['Змагання:', tournament.name, '', '', '', ''],
        ['Дата і місце:', tournament.place, '', '', '', tournament.tdate],
        ['Категорія:', competition.category.name, 'Стать:', competition.get_gender_display(), 'Вік:', competition.age]
    ]
    
    col1 = 2.5 * cm
    col2 = width * 0.35
    col3 = 1.5 * cm
    col4 = 2.5 * cm
    col5 = 1 * cm
    col6 = width * 0.2
    
    row1 = 1.2 * cm
    row2 = 0.65 * cm
    row3 = 0.3 * cm
    row4 = 0.6 * cm
        
    
    upper_table = Table(upper_table_data, colWidths=[col1, col2, col3, col4, col5, col6], rowHeights=[row1, row2, row3, row4, row4, row4])
    upper_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (5, 0)),
        ('ALIGN', (0, 0), (5, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (5, 0), 11),
        
        ('SPAN', (0, 1), (5, 1)),
        ('ALIGN', (0, 1), (5, 1), 'CENTER'),   
             
        ('SPAN', (1, 3), (5, 3)),   
             
        ('SPAN', (1, 4), (4, 4)),        
        ('GRID', (0, 0), (-1, -1), 0.2, colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
        ('FONTSIZE', (0, 2), (0, -1), 9),
        
        ('FONTSIZE', (0, 3), (0, 5), 7),
        ('FONTSIZE', (2, 5), (2, 5), 7),
        ('FONTSIZE', (4, 5), (4, 5), 7),
        
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 3), (0, 5), 4),
        ('TOPPADDING', (2, 5), (2, 5), 4),
        ('TOPPADDING', (4, 5), (4, 5), 4),
        
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    # Отрисовка верхней таблицы (20 мм от верха страницы, с учетом заголовка)
    upper_table_height = 110  # примерная высота таблицы из 5 строк
    upper_table.wrapOn(c, width, height)
    upper_table.drawOn(c, margin, height - margin - upper_table_height)
    
    #TAB NET
    
    
    # NET
    if len(participants) >= 2:
        draw_tab_net(c, participants)
        draw_net(c, participants)
        drawParticipants(c, participants)
    if len(participants) > 3:
        drawThird(c, participants)
    
    # НИЖНЯЯ ЧАСТЬ
    
    # Таблица в нижней части
    lower_table_data = [
        ['1.', ''],
        ['2.', ''],
        ['3.', ''],
        ['4.', '']
    ]
    
    lower_table = Table(lower_table_data, colWidths=[1*cm, 7*cm], rowHeights=[.5*cm, .5*cm, .5*cm, .5*cm])
    lower_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1,-1), 0.5, colors.black)
    ]))
    
    # Отрисовка нижней таблицы (20 мм от низа страницы)
    lower_table_width = 8 * cm
    lower_table_height = 70  # примерная высота таблицы из 4 строк
    lower_table.wrapOn(c, width, height)
    lower_table.drawOn(c, width - margin - lower_table_width, 0 + margin + 40)
    
    final_table_data = [
        [tournament.referre, '', tournament.secretary],
        ['Головний суддя:', '', 'Головна секретарка:'],
    ]
    
    final_table_col = (width - (2 * margin) - 1 * cm) / 2
    
    final_table = Table(final_table_data, colWidths=[final_table_col, 1*cm, final_table_col])
    final_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
        ('FONTSIZE', (0, 0), (2, 0), 10),
        ('FONTSIZE', (0, 1), (2, 1), 8),
        ('LINEABOVE',(0,1),(0,1),0.5,colors.black),
        ('LINEABOVE',(2,1),(2,1),0.5,colors.black),
    ]))
    
    
    # final_table_height = 30
    final_table.wrapOn(c, width, height)
    final_table.drawOn(c, margin, margin)
    
    
    # Сохраняем документ
    c.save()
    buffer.seek(0)
    return buffer
    
    
def protocols_generate(request, pk:str):
    trn_id = int(pk)
    tournament = models.Tournament.objects.get(idx=trn_id)
    competitions = models.Competition.objects.filter(Q(tournament_id=trn_id))
    
    merger = PdfMerger()
    
    for competition in competitions:
        com_id = competition.idx
        
        participants = models.CompetitionParticipants.objects.filter(Q(competition_id=com_id))
        participants_list = []
        
        for cp in participants:
            participants_list.append(cp.participant.name)
            
        print('-----------')
        print('Tournament: ', tournament.name)
        print('Competition: ', competition.__str__())
        print('Participants: ', participants_list)
        print('----***----')
        
        page_pdf = create_document(tournament, competition, participants_list)
        pdf_reader = PdfReader(page_pdf) 
        merger.append(pdf_reader)
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="protocols.pdf"'
    
    # final_pdf = "protocol.pdf"
    # merger.write(final_pdf)
    
    merger.write(response)
    merger.close()
    
    # print(f"Создан документ: {final_pdf}")
    
    return response
        
        
    

