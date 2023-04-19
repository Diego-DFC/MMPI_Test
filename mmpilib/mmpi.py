# -*- coding:utf-8 -*-

# 版权所有 (C) 2018.6.25 金盛羽。保留所有权利。
# Copyright 2018.6.25 Shengyu Jin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
本模块主用于处理和MMPI测试相关的函数功能，其中包含一份完整的MMPI测试问卷
This module is mainly for processing functions about MMPI, including
a complete questionnaire.
"""

import time
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.styles import Font, Alignment

# for debug
from random import randint

# 指导语
# Instruction
Ins1 = """-----------------------------------------------------------------
                       明尼苏达多项人格测验                      
       Minnesota Multiphasic Per-sonality Inventory (MMPI)       
-----------------------------------------------------------------
Breve descripción: el Inventario de Personalidad Múltiple de Minnesota (MMPI) fue desarrollado por S. R. Hathaway y J. C. McKinley, profesores de la Universidad de Minnesota, en 1942.
（S. R. Hathaway y J. C. McKinley en 1942.
Puede utilizarse para comprobar el tipo de personalidad de una persona normal o para distinguir entre una persona normal y una persona con una enfermedad mental o psiquiátrica. A finales del siglo pasado
A finales del siglo pasado, sobre la base de muchos años de investigación y la investigación práctica por el Sr. Ji Jumao y otros, el cuestionario MMPI y el Inventario Psicológico Frecuente (IPF) fueron desarrollados para su uso en China.
El cuestionario y la norma del MMPI se utilizan en China desde 1980 y se han extendido su uso en los últimos años.
Los resultados demuestran que la prueba tiene un cierto grado de fiabilidad y validez en China y posee un alto valor clínico de referencia.
-----------------------------------------------------------------
Recordatorio importante: Este test es un instrumento psicométrico profesional con valor de referencia clínico y debe ser utilizado e interpretado con precaución por los profesionales pertinentes.
Debe ser utilizado e interpretado bajo la orientación de un profesional pertinente, ¡y debe ser utilizado con precaución por particulares!                                 
-----------------------------------------------------------------"""

Ins2 = """-----------------------------------------------------------------
Orientación: Este cuestionario consta de una serie de preguntas relevantes para usted.
si coincide con su comportamiento, sentimientos, actitudes u opiniones actuales. En caso afirmativo, marque un "1"; en caso contrario, marque un "0".
Escriba un "0" en caso afirmativo, en caso contrario escriba un "0" y confirme pulsando la tecla "Intro" para completar la pregunta. Escriba sus primeras impresiones lo antes posible tras leer la pregunta.
No dedique demasiado tiempo a reflexionar sobre cada pregunta. Las personalidades varían y no existe una respuesta correcta o incorrecta.
No hay que preocuparse por lo que es correcto o incorrecto, bueno o malo, simplemente responda como mejor le parezca.
-----------------------------------------------------------------
Ejemplo de respuesta:
x. Mi sexo es
1. masculino 0. femenino
> 1
-----------------------------------------------------------------"""


# Preguntas del cuestionario MMPI de 566 ítems
# 566 questions of MMPI questionnaire
Que = {
    1: 'Me gusta leer noticias sobre tecnología',
    2: 'Tengo buen apetito',
    3: 'Cuando me levanto por la mañana, casi siempre me siento bien dormido y con la cabeza despejada',
    4: 'Creo que me gustaría el trabajo de bibliotecario',
    5: 'Me despierto fácilmente cuando duermo',
    6: 'Me gusta leer noticias relacionadas con la delincuencia',
    7: 'A menudo tengo las manos y los pies muy calientes',
    8: 'Mi vida diaria está llena de cosas que me interesan',
    9: 'Puedo trabajar (estudiar) tan bien como antes',
    10: 'Siempre hay algo en mi garganta que parece estar bloqueado',
    11: 'Uno debería entender sus sueños y obtener orientación o advertencias de ellos',
    12: 'Me gusta leer novelas policíacas o de misterio',
    13: 'Siempre trabajo en situaciones muy estresantes',
    14: 'Tengo diarrea al menos una o dos veces al mes',
    15: 'De vez en cuando se me ocurre algo demasiado malo que decir',
    16: 'Estoy convencido de que la vida no es justa conmigo',
    17: 'Mi padre es un buen hombre',
    18: 'Rara vez estoy estreñido',
    19: 'Cuando encuentro un nuevo trabajo, siempre me gusta que me digan en confianza a quién debo dirigirme',
    20: 'Mi vida sexual es satisfactoria',
    21: 'A veces tengo muchas ganas de irme de casa',
    22: 'A veces lloro y río durante un rato sin poder controlarme',
    23: 'Tengo náuseas y vómitos',
    24: 'Parece que nadie me entiende',
    25: 'Creo que me gustaría ser cantante',
    26: 'Cuando estoy en una situación difícil, creo que es mejor no hablar',
    27: 'A veces siento que estoy poseído por un demonio',
    28: 'Cuando alguien se mete conmigo, doy por sentado que debo tomar represalias siempre que tenga la oportunidad',
    29: 'Sufro de hiperacidez varias veces por semana',
    30: 'A veces sólo quiero decir palabrotas',
    31: 'Tengo pesadillas cada pocas noches',
    32: 'Me cuesta concentrarme en una tarea',
    33: 'He tenido experiencias muy raras y extrañas',
    34: 'Toso mucho',
    35: 'Habría conseguido más si alguien no hubiera trabajado en mi contra',
    36: 'Rara vez me preocupo por mi salud',
    37: 'Nunca he tenido problemas por mi sexualidad',
    38: 'Cuando era niño, hubo un tiempo en que cometí algún hurto',
    39: 'A veces quería romper cosas',
    40: 'Muchas veces prefiero sentarme y pensar que hacer algo',
    41: 'No quiero hacer nada durante días, semanas o meses porque no me entra en la cabeza',
    42: 'A mi familia no le gusta el trabajo que he elegido (o la carrera que voy a elegir)',
    43: 'No duermo bien y me despierto con facilidad',
    44: 'A menudo siento que me duele la cabeza por todas partes',
    45: 'A veces digo mentiras',
    46: 'Ahora tengo más juicio que nunca',
    47: 'Al menos una o dos veces por semana, de repente siento calor por todo el cuerpo sin motivo aparente',
    48: 'Cuando estoy con gente, me altero cuando oigo hablar de cosas extrañas e inusuales',
    49: 'Sería mejor que se abolieran todas las leyes',
    50: 'A veces siento que mi alma ha abandonado mi cuerpo',
    51: 'Mi cuerpo está tan sano como el de la mayoría de mis amigos',
    52: 'Cuando me encuentro con compañeros de clase o amigos poco comunes, finjo no verlos a menos que me saluden primero',
    53: 'Un sacerdote (un monje, un sacerdote taoísta, un cura, un imán, etc.) puede curar a un enfermo rezando y poniendo la mano en la cabeza del paciente',
    54: 'Le caigo bien a casi todo el mundo que me conoce',
    55: 'Nunca me han dolido el pecho ni el corazón',
    56: 'Cuando era niño, me castigaban en el colegio por ser un niño travieso',
    57: 'Me relaciono con la gente en cuanto la conozco, o tengo una personalidad interesada',
    58: 'Todo está dispuesto por Dios o por el destino',
    59: 'A menudo tengo que seguir las órdenes de personas que en realidad no son tan buenas como yo',
    60: 'No leo todos los editoriales del periódico todos los días',
    61: 'Nunca he tenido una vida normal',
    62: 'A menudo tengo la sensación de que algunas partes del cuerpo me arden, me hormiguean, se arrastran o se me duermen',
    63: 'No tengo dificultades para controlar mis movimientos intestinales',
    64: 'A veces hago una cosa una y otra vez hasta que los demás se aburren',
    65: 'Quiero a mi padre',
    66: 'Puedo ver cosas, animales o personas a mi alrededor que nadie más puede ver',
    67: 'Me gustaría ser tan feliz como los demás',
    68: 'Casi nunca me duele la nuca',
    69: 'Las personas de mi mismo sexo me resultan muy atractivas',
    70: 'Antes me gustaba jugar a juegos como 'lanzar pañuelos'',
    71: 'Creo que a muchas personas les gusta exagerar sus desgracias para obtener simpatía y ayuda de los demás',
    72: 'Me preocupa sentirme mal del corazón (del estómago) cada pocos días o a menudo',
    73: 'Soy una persona importante',
    74: 'Siempre deseo ser mujer, pero nunca lamento ser mujer',
    75: 'A veces me enfado',
    76: 'A menudo me siento pesimista y decepcionada',
    77: 'Me gusta leer novelas románticas',
    78: 'Me gusta la poesía',
    79: 'Mis sentimientos no se hieren fácilmente',
    80: 'A veces juego con animales',
    81: 'Creo que me gustaría trabajar de guarda forestal',
    82: 'Cuando discuto con la gente, a menudo no puedo competir con ellos',
    83: 'Cualquiera que pueda y quiera trabajar duro tendrá muchas posibilidades de éxito',
    84: 'Hoy en día, me resulta fácil renunciar a mí mismo',
    85: 'A veces me atraen mucho las cosas de los demás, como zapatos, guantes, etc., y aunque no me sirven para nada, siempre quiero tocarlas o robarlas',
    86: 'Me falta confianza en mí mismo',
    87: 'Me gustaría ser florista',
    88: 'Siempre siento que merece la pena vivir',
    89: 'Hay que debatir mucho para convencer a la mayoría de la gente de la verdad',
    90: 'A veces dejo para mañana lo que debería haber hecho hoy',
    91: 'No me importa que la gente se burle de mí',
    92: 'Quiero ser enfermera',
    93: 'Creo que la mayoría de la gente está dispuesta a mentir para ascender',
    94: 'He hecho muchas cosas de las que luego me arrepiento',
    95: 'Voy a la iglesia (o a menudo a un lugar religioso como un templo) casi todas las semanas',
    96: 'Rara vez discuto con mi familia',
    97: 'A veces tengo un fuerte impulso de hacer algo sorprendente o perjudicial',
    98: 'Creo que el bien se recompensa con el bien y el mal con el mal',
    99: 'Me gusta ir a fiestas animadas',
    100: 'Me he encontrado con mil problemas que me hacen sentir indeciso',
    101: 'Creo que las mujeres deberían tener la misma libertad que los hombres en lo que se refiere a su sexualidad',
    102: 'Creo que lo más difícil es controlarme',
    103: 'Rara vez sufro calambres o temblores musculares',
    104: 'Parece que todo me da igual',
    105: 'A veces pierdo los nervios cuando no me encuentro bien',
    106: 'Siempre tengo la sensación de haber hecho algo mal o de haber cometido algún delito',
    107: 'A menudo soy feliz',
    108: 'A menudo tengo la cabeza hinchada y la nariz tapada',
    109: 'Algunas personas son tan prepotentes que tengo que luchar contra ellas aunque sé que tienen razón',
    110: 'Alguien quiere hacerme daño',
    111: 'Nunca he hecho nada peligroso por puro placer',
    112: 'A menudo pienso que debo atenerme a lo que creo que es correcto',
    113: 'Creo en el Estado de Derecho',
    114: 'A menudo siento como si tuviera una banda alrededor de la cabeza',
    115: 'Creo en un 'más allá' después de la muerte',
    116: 'Prefiero los partidos o competiciones en los que he apostado',
    117: 'La mayoría de la gente es sincera sobre todo porque tiene miedo de ser vista por los demás',
    118: 'Cuando iba al colegio, a veces me llamaba el director por ser travieso',
    119: 'Siempre hablé ni muy rápido ni muy despacio, ni muy arrastrado ni muy ronco',
    120: 'Soy mucho más disciplinado cuando salgo a comer con mis amigos que cuando estoy en casa',
    121: 'Creo que alguien me está apuñalando por la espalda',
    122: 'Parece que soy tan astuto y capaz como la gente que me rodea',
    123: 'Creo que alguien me está siguiendo',
    124: 'La mayoría de la gente está más dispuesta a utilizar medios poco escrupulosos para obtener ventajas que a perder la oportunidad',
    125: 'Tengo muchos problemas de estómago',
    126: 'Me gusta el teatro o el cabaret',
    127: 'Sé quién es el responsable de mis problemas',
    128: 'Cuando veo sangre, ni me asusto ni me siento incómodo',
    129: 'A menudo no sé por qué estoy tan enfadado o quejica',
    130: 'Nunca he vomitado sangre, ni he tenido una hemoptisis',
    131: 'No me preocupa ponerme enfermo',
    132: 'Me gusta plantar flores o coleccionarlas',
    133: 'Nunca he tenido una conducta sexual inapropiada',
    134: 'A veces mis pensamientos van demasiado deprisa para poder expresarlos',
    135: 'Si pudiera ver una película gratis sin comprar entrada y nadie se diera cuenta, probablemente lo haría',
    136: 'Si la gente me trata bien, a menudo sospecho que tienen motivos ocultos',
    137: 'Creo que mi vida familiar es tan feliz y alegre como la de muchas personas que conozco',
    138: 'Las críticas y las reprimendas me ponen muy triste',
    139: 'A veces siento que tengo que hacerme daño a mí mismo o a los demás',
    140: 'Me gusta cocinar y hervir la comida',
    141: 'Mi comportamiento está dictado principalmente por los hábitos de los que me rodean',
    142: 'A veces pienso que soy un inútil',
    143: 'De pequeño formaba parte de una pandilla que compartía los buenos y los malos momentos',
    144: 'Me gustaba ser soldado',
    145: 'A veces quiero pelearme con la gente porque sí',
    146: 'Me gusta pasear y me molestaría que no me dejaran hacerlo',
    147: 'He perdido muchas buenas oportunidades porque a menudo soy incapaz de tomar una decisión',
    148: 'Me impaciento si alguien me pide consejo o me interrumpe cuando estoy haciendo algo importante',
    149: 'Antes llevaba un diario',
    150: 'Cuando juego, sólo quiero ganar y no perder',
    151: 'Alguien intenta envenenarme',
    152: 'La mayoría de las noches duermo sin que me perturbe ningún pensamiento',
    153: 'La mayor parte del tiempo en los últimos años he gozado de buena salud',
    154: 'Nunca he tenido un tic',
    155: 'Ahora no he ganado ni perdido peso',
    156: 'Hubo un tiempo en que no me acordaba de nada de lo que había hecho',
    157: 'Siento que a menudo me castigan sin motivo',
    158: 'Lloro con facilidad',
    159: 'No entiendo lo que leo tan bien como antes',
    160: 'Nunca en mi vida me he sentido mejor que ahora',
    161: 'A veces siento que me duele la parte superior de la cabeza cuando me la toco',
    162: 'Odio cuando la gente me pilla de una forma incorrecta y tengo que admitir mi derrota',
    163: 'No me canso fácilmente',
    164: 'Me gusta investigar y leer sobre temas relacionados con mi trabajo actual',
    165: 'Me gusta conocer a gente importante, eso también me hace sentir importante',
    166: 'Me da miedo mirar desde arriba',
    167: 'No me pondría nervioso si alguien de mi familia infringiera la ley',
    168: 'Tengo un pequeño problema cerebral',
    169: 'No me da miedo administrar el dinero',
    170: 'No me importa lo que la gente piense de mí',
    171: 'Me sentiría incómodo si me pidieran que hiciera lo mismo en una fiesta, aunque alguien sea el centro de atención',
    172: 'A menudo tengo que intentar no parecer tímido',
    173: 'Antes me gustaba el colegio',
    174: 'Nunca me he desmayado',
    175: 'Rara vez me mareo',
    176: 'No me dan miedo las serpientes',
    177: 'Mi madre es una buena persona',
    178: 'Parece que tengo buena memoria',
    179: 'Me molestan las preguntas sobre sexo',
    180: 'Creo que no sé qué decir cuando conozco a alguien',
    181: 'Cuando me aburro, me meto en líos y me divierto',
    182: 'Tengo miedo de volverme loco',
    183: 'Estoy en contra de dar dinero a los mendigos',
    184: 'A menudo oigo hablar sin saber de dónde viene',
    185: 'Mi oído es aparentemente tan bueno como el de la mayoría de la gente',
    186: 'A menudo me tiemblan las manos cuando voy a hacer algo',
    187: 'Mis manos no se han vuelto torpes e incompetentes',
    188: 'Puedo leer durante mucho tiempo sin que se me cansen los ojos',
    189: 'Muchas veces me siento débil',
    190: 'Rara vez me duele la cabeza',
    191: 'A veces, cuando me siento avergonzado, sudo mucho y esto me angustia mucho',
    192: 'Nunca me he sentido incapaz de mantener el equilibrio al caminar',
    193: 'No tengo asma como enfermedad',
    194: 'Ha habido ocasiones en las que de repente he sido incapaz de controlar mis movimientos o mi habla, pero mi mente estaba clara en ese momento',
    195: 'No me gusta toda la gente que conozco',
    196: 'Me gusta visitar lugares en los que nunca he estado antes',
    197: 'Alguien sigue intentando quitarme algo',
    198: 'Casi nunca pienso en nada',
    199: 'Deberíamos contar a nuestros hijos las principales cosas que debemos saber sobre el sexo',
    200: 'Alguien intenta robarme mis ideas y planes',
    201: 'Me gustaría no ser tan tímido como soy ahora',
    202: 'Creo que soy una persona condenada',
    203: 'Si fuera periodista, preferiría dedicarme al mundo del espectáculo',
    204: 'Me gusta ser periodista',
    205: 'A veces no puedo evitar querer robar algo',
    206: 'Creo en Dios más que la mayoría de la gente',
    207: 'Me gustan muchos tipos de juegos o entretenimientos',
    208: 'Me gusta reírme con personas del sexo opuesto',
    209: 'Creo que mis pecados son imperdonables',
    210: 'Todo sabe igual cuando se come',
    211: 'Puedo dormir durante el día, pero no puedo dormir por la noche',
    212: 'La gente de mi familia me trata como a un niño y no como a un adulto',
    213: 'Cuando camino, cruzo las costuras de la acera con mucho cuidado',
    214: 'Nunca me ha molestado nada que crezca en mi piel',
    215: 'Solía beber en exceso',
    216: 'A mi familia le falta amor y calor en comparación con las familias de otras personas',
    217: 'A menudo tengo la sensación de estar preocupado por algo',
    218: 'No me siento especialmente mal cuando veo que torturan animales',
    219: 'Creo que me gustaría trabajar como constructor',
    220: 'Quiero a mi madre',
    221: 'Me gusta la ciencia',
    222: 'Aunque luego no pueda devolver un favor, pediría ayuda a un amigo',
    223: 'Me gusta mucho cazar',
    224: 'Mis padres suelen poner objeciones a la gente que sale conmigo',
    225: 'A veces cotilleo sobre la gente',
    226: 'En mi familia hay algunas personas cuyas costumbres me resultan muy molestas',
    227: 'Me han dicho que me levanto dormido y soy sonámbulo',
    228: 'A veces creo que puedo tomar decisiones con mucha facilidad',
    229: 'Me gusta estar en varios grupos a la vez',
    230: 'Nunca me falta el aire',
    231: 'Me gusta hablar de cuestiones de género',
    232: 'Una vez me propuse llevar una vida responsable y he tenido cuidado de hacerlo',
    233: 'A veces impido que la gente haga ciertas cosas, no por las implicaciones de las mismas, sino porque es 'moralmente' correcto que intervenga',
    234: 'Me enfado con facilidad, pero me calmo rápidamente',
    235: 'Soy independiente y no estoy vinculado a la familia',
    236: 'Tengo muchas cosas en la cabeza',
    237: 'Casi todos mis familiares simpatizan conmigo',
    238: 'A veces estoy muy irritable e inquieto',
    239: 'Una vez me desenamoré',
    240: 'Nunca pienso dos veces en mi apariencia',
    241: 'A menudo sueño con cosas indecibles',
    242: 'Creo que no soy más sensible que los demás',
    243: 'Tengo poco o ningún dolor en ninguna parte',
    244: 'Mi forma de actuar se malinterpreta con facilidad',
    245: 'Mis padres y mi familia me critican demasiado',
    246: 'A menudo tengo manchas rojas en el cuello',
    247: 'Tengo motivos para estar celoso de algunos miembros de mi familia',
    248: 'A veces me siento muy feliz sin ninguna razón, incluso cuando las cosas no van bien',
    249: 'Creo en un mundo de demonios y en el infierno después de la muerte',
    250: 'No culpo a alguien por querer coger todas las cosas del mundo que pueda',
    251: 'Una vez tuve un momento en el que de repente me quedé helado (congelado) y dejé de moverme, sin saber lo que pasaba a mi alrededor',
    252: 'A nadie le importa lo que les pasa a los demás',
    253: 'Algunas personas hacen cosas que me parecen mal, pero aún así puedo ser amable con ellas',
    254: 'Me gusta pasar el tiempo con gente con la que se puede bromear',
    255: 'En época de elecciones, a veces elijo a gente que no conozco bien',
    256: 'Sólo las 'viñetas' del periódico son las más divertidas',
    257: 'En todo lo que hago, espero tener éxito',
    258: 'Creo en Dios',
    259: 'Me cuesta empezar a hacer algo',
    260: 'Fui un estudiante estúpido en el colegio',
    261: 'Si fuera pintor, preferiría pintar flores',
    262: 'No sufro por no ser guapo',
    263: 'Sudo con facilidad incluso en los días fríos', .
    264: 'Tengo mucha confianza en mí mismo',
    265: 'Es más seguro no fiarse de nadie',
    266: 'Al menos una o dos veces por semana me excito mucho',
    267: 'No sé qué decir cuando hay mucha gente',
    268: 'Cuando estoy deprimido, siempre hay algo que me anima',
    269: 'Puedo hacer que la gente me tenga miedo con facilidad, y a veces lo hago a propósito para que estén contentos',
    270: 'Nunca me preocupo de si las puertas y ventanas están cerradas o atrancadas cuando estoy fuera de casa',
    271: 'No culpo a una persona que intimida a otra que ha hecho el ridículo',
    272: 'A veces tengo mucha energía', .
    273: 'Tengo entumecimiento en uno o dos lugares de la piel',
    274: 'Mi vista es tan buena como en años anteriores',
    275: 'Alguien controla mi mente',
    276: 'Me gustan los niños',
    277: 'A veces admiro tanto el ingenio de un estafador que incluso espero que se salga con la suya',
    278: 'A menudo siento que algunos desconocidos me miran con ojos críticos',
    279: 'Bebo mucha agua todos los días',
    280: 'La mayoría de la gente hace amigos porque les son útiles',
    281: 'Creo que rara vez me pitan los oídos',
    282: 'Normalmente quiero a la gente de mi familia, pero a veces la odio',
    283: 'Si fuera periodista, preferiría cubrir deportes',
    284: 'Estoy seguro de que la gente habla de mí',
    285: 'A veces me río con chistes verdes',
    286: 'Me siento más feliz cuando estoy solo',
    287: 'Me asusto mucho menos que mis amigos',
    288: 'Las náuseas y los vómitos me hacen sentir desgraciado',
    289: 'Me repugna la ley cuando un criminal puede ser exonerado por un abogado elocuente',
    290: 'Siempre trabajo en una situación muy estresante',
    291: 'Al menos una o dos veces en mi vida he tenido la sensación de que alguien me había ordenado hacer algo por hipnosis',
    292: 'Generalmente soy reacio a hablar con la gente a menos que ellos hablen primero',
    293: 'Alguien ha intentado influir en mi mente',
    294: 'Nunca he infringido la ley',
    295: 'Me gusta leer novelas como El sueño de la cámara roja',
    296: 'Hay veces que me siento muy feliz sin ninguna razón',
    297: 'Me gustaría no tener más pensamientos de carácter sexual',
    298: 'Si algunas personas se meten en problemas, más vale que antes inventen una mentira y no cambien su historia',
    299: 'Creo que soy más emocional que la mayoría de la gente',
    300: 'En mi vida me ha gustado una muñeca',
    301: 'Muchas veces la vida ha sido una lucha para mí',
    302: 'Nunca he tenido problemas con mi sexualidad',
    303: 'Soy tan sensible a ciertas cosas que no puedo mencionarlas',
    304: 'En el colegio me resulta muy difícil hablar en clase',
    305: 'Incluso cuando estoy con gente, a menudo me siento solo',
    306: 'Recibí toda la compasión que merecía',
    307: 'Me niego a jugar a cosas que no sé hacer bien',
    308: 'A veces tengo muchas ganas de irme de casa',
    309: 'Hago amigos casi tan fácilmente como cualquier otra persona',
    310: 'Mi vida sexual es satisfactoria',
    311: 'Cuando era niño, hubo un tiempo en que cometí pequeños robos',
    312: 'No me gusta tener gente a mi alrededor',
    313: 'Alguien que no guarda sus objetos de valor y, por tanto, provoca que otros roben, es tan culpable como un ladrón',
    314: 'De vez en cuando se me ocurre algo demasiado malo que decir',
    315: 'Estoy convencido de que la vida ha sido injusta conmigo',
    316: 'Creo que casi todo el mundo, para evitar problemas, dice alguna mentira',
    317: 'Soy más sensible que la mayoría de la gente',
    318: 'Mi vida cotidiana está llena de cosas que me interesan',
    319: 'La mayoría de la gente, en el fondo, no está dispuesta a dar un paso adelante y ayudar a los demás',
    320: 'Algunos de mis sueños tienen que ver con temas sexuales',
    321: 'Me avergüenzo con facilidad',
    322: 'Me preocupo por el dinero y la carrera',
    323: 'He tenido experiencias muy especiales y extrañas',
    324: 'Nunca me he enamorado de nadie',
    325: 'Algunas personas de mi familia hacen cosas que me sorprenden',
    326: 'A veces lloro y río durante un rato, y ni siquiera puedo controlarme',
    327: 'Mi madre o mi padre me piden a menudo que les obedezca, aunque yo piense que no es razonable',
    328: 'Me cuesta concentrarme en una tarea',
    329: 'Casi nunca sueño',
    330: 'Nunca he estado paralizado ni he sentido una gran debilidad muscular',
    331: 'Habría conseguido más si alguien no se me hubiera opuesto',
    332: 'Incluso cuando no estoy resfriado, a veces me cuesta emitir sonidos o me cambia la voz',
    333: 'Parece que nadie me entiende',
    334: 'A veces siento olores extraños',
    335: 'No consigo concentrarme en una cosa',
    336: 'Me impaciento con la gente con mucha facilidad',
    337: 'Estoy ansioso por algo o por alguien casi todo el día',
    338: 'Me preocupo por mucho más de lo que debería',
    339: 'La mayor parte del tiempo pienso que estaría mejor muerto',
    340: 'A veces me emociono tanto que me cuesta dormir',
    341: 'A veces mi sentido del oído es tan agudo que me molesta',
    342: 'Olvido inmediatamente lo que me dicen',
    343: 'Me lo pienso dos veces antes de hacer cosas, incluso triviales',
    344: 'A veces doy un rodeo para evitar encontrarme con alguien',
    345: 'A menudo tengo la sensación de que nada es real',
    346: 'Tengo la costumbre de señalar cosas sin importancia, como postes de teléfono en la carretera, etc.',
    347: 'No tengo ningún deseo real de hacer daño a mis enemigos',
    348: 'Desconfío de las personas que están demasiado cerca de mí',
    349: 'Tengo pensamientos extraños y peculiares',
    350: 'Cuando estoy solo, oigo ruidos extraños',
    351: 'Me siento distraído cuando tengo que salir de casa por poco tiempo',
    352: 'Tengo miedo de cosas o personas, aunque sé que no me harán daño',
    353: 'No me da miedo entrar solo si ya hay gente hablando en casa',
    354: 'Me da miedo utilizar un cuchillo o algo afilado',
    355: 'A veces me gusta torturar a las personas que quiero',
    356: 'Parece que me cuesta más concentrarme que a los demás',
    357: 'Hay veces que dejo lo que estoy haciendo porque me siento muy mal con mis capacidades',
    358: 'A menudo tengo en la cabeza palabras malas que me dan miedo y no puedo quitármelas de la cabeza',
    359: 'A veces algunos pensamientos insignificantes me persiguen y me hacen sentir incómodo durante días',
    360: 'Casi todos los días ocurre algo que me asusta',
    361: 'Siempre me tomo las cosas más en serio',
    362: 'Soy más sensible que la mayoría de la gente', .
    363: 'A veces me gusta que mi amado me torture',
    364: 'Algunas personas hablan de mí de forma insultante y desagradable',
    365: 'Siempre me siento incómodo cuando estoy en casa',
    366: 'A menudo me siento solo aunque esté con gente',
    367: 'No soy especialmente tímido ni formal',
    368: 'A veces mi mente parece ir más lenta de lo normal',
    369: 'En situaciones sociales, casi siempre me siento solo o con otra persona y no me meto entre la multitud',
    370: 'La gente suele decepcionarme',
    371: 'Me gusta ir a bailes',
    372: 'A veces me resulta demasiado difícil superarlo',
    373: 'A menudo pienso: 'Si pudiera volver a ser niño'',
    374: 'Si tuviera la oportunidad, podría hacer algo grande por el mundo',
    375: 'A menudo me encuentro con supuestos expertos que no son mejores que yo',
    376: 'Cuando oigo que alguien que conozco ha tenido éxito, siento que yo he fracasado',
    377: 'Si tuviera la oportunidad, sería un buen líder del pueblo',
    378: 'Las historias desagradables me hacen sentir avergonzado',
    379: 'Por lo general, la gente pide a los demás que les respeten más, pero rara vez lo hacen ellos mismos',
    380: 'Siempre quiero recordar las buenas historias y contárselas a los demás',
    381: 'Me gusta jugar a cosas que no gano ni pierdo',
    382: 'Me gusta socializar para estar con la gente', .
    383: 'Me gusta estar en un lugar lleno de gente',
    384: 'Mis preocupaciones desaparecen cuando estoy con un grupo de amigos felices',
    385: 'Nunca me involucro cuando la gente cotillea sobre mis socios',
    386: 'En cuanto empiezo algo, me cuesta dejarlo, aunque sea temporalmente',
    387: 'No me cuesta orinar ni controlarlo',
    388: 'A menudo me doy cuenta de que los demás están celosos de mis buenas ideas porque no se les ocurrieron a ellos primero',
    389: 'Siempre que puedo, evito las multitudes',
    390: 'No me da miedo encontrarme con desconocidos',
    391: 'Recuerdo que solía fingir estar enfermo para evitar algo',
    392: 'Suelo hablar con desconocidos en trenes y autobuses',
    393: 'Cuando las cosas no van bien, quiero rendirme inmediatamente', .
    394: 'Me gusta que la gente sepa lo que pienso de las cosas',
    395: 'Hay veces que me siento con tanta energía que no necesito dormir durante días',
    396: 'No me avergüenzo si me piden que tome la iniciativa en una reunión o que dé mi opinión sobre algo que conozco',
    397: 'Me gustan las fiestas y los actos sociales',
    398: 'Siempre retrocedo ante las dificultades o el peligro',
    399: 'Me resulta fácil abandonar algo que quería hacer en un principio si los demás no creen que merezca la pena',
    400: 'No tengo miedo al fuego',
    401: 'No tengo miedo al agua',
    402: 'Suelo pensar detenidamente antes de tomar una decisión',
    403: 'Qué maravilloso es vivir en estos tiempos llenos de color',
    404: 'A menudo se malinterpretan mis buenas intenciones cuando intento corregir los errores de la gente y ayudarles',
    405: 'No me cuesta tragar',
    406: 'A veces evito quedar con la gente porque tengo miedo de hacer o decir algo de lo que luego me arrepienta',
    407: 'Suelo estar muy tranquilo y no me excito con facilidad',
    408: 'No muestro mis sentimientos con facilidad, de modo que la gente me hace daño y ni siquiera lo sabe',
    409: 'A veces me agoto asumiendo demasiadas cosas',
    410: 'Me gusta hacer a los demás lo que me hacen a mí',
    411: 'La religión no me preocupa',
    412: 'No tengo miedo de ir al médico cuando estoy enfermo o herido',
    413: 'He pecado y merezco un castigo severo',
    414: 'Me tomo las decepciones tan en serio que no siempre puedo olvidarlas',
    415: 'Tengo una gran aversión a hacer mi trabajo con prisas',
    416: 'Aunque sé que puedo hacer las cosas, también tengo miedo de que la gente me vea hacerlo',
    417: 'Me enfado si alguien se pone delante de mí en la cola y lo acuso',
    418: 'A veces siento que no sirvo para nada',
    419: 'De pequeño, solía faltar al colegio',
    420: 'Tuve una experiencia religiosa poco habitual',
    421: 'Alguien de mi familia es muy sensible',
    422: 'Me avergüenzan las ocupaciones que han tenido algunos miembros de mi familia',
    423: 'Me gusta mucho (o me ha gustado) pescar',
    424: 'Casi siempre tengo hambre',
    425: 'A menudo tengo sueños',
    426: 'A veces tengo que tratar con gente maleducada o desagradable de forma grosera',
    427: 'Suelo interesarme por diferentes aficiones en lugar de dedicarme a una durante mucho tiempo',
    428: 'Me gusta leer los editoriales de los periódicos',
    429: 'Me gusta escuchar discursos sobre temas serios',
    430: 'Me atrae fácilmente el sexo opuesto',
    431: 'Me preocupan bastante las posibles desgracias',
    432: 'Tengo fuertes opiniones políticas',
    433: 'He tenido compañeros imaginarios',
    434: 'Me gustaría ser motociclista',
    435: 'Me suele gustar trabajar con mujeres',
    436: 'Estoy seguro de que sólo una religión es verdadera',
    437: 'Está bien infringir la ley siempre que no la infrinjas',
    438: 'Hay personas tan molestas que me alegro en secreto de que reciban su merecido',
    439: 'Me pongo nervioso cuando tengo que esperar',
    440: 'Cuando soy feliz, me decepciona ver a los demás deprimidos',
    441: 'Me gustan las mujeres altas',
    442: 'Hay veces que pierdo el sueño por mis preocupaciones',
    443: 'Me resulta fácil rendirme si la gente piensa que no estoy haciendo algo bien',
    444: 'No quiero corregir a la gente que expresa opiniones ignorantes e incultas',
    445: 'Cuando era joven (de niño), me gustaba buscar emociones',
    446: 'La policía suele ser honesta',
    447: 'Cuando alguien no está de acuerdo conmigo, hago lo que puedo para convencerle',
    448: 'Me siento incómodo si alguien me mira en la calle, en un coche o en una tienda',
    449: 'No me gusta ver fumar a las mujeres',
    450: 'Raramente sufro de melancolía',
    451: 'Siempre soy incapaz de corregir a alguien si hace comentarios estúpidos e ignorantes sobre cosas que conozco',
    452: 'Me gusta hacer bromas sobre la gente',
    453: 'Cuando era niño, no me gustaba unirme a una banda',
    454: 'Era feliz viviendo solo en una cabaña en las montañas o en el viejo bosque',
    455: 'Mucha gente dice que soy una persona aguda',
    456: 'Si un hombre infringe una ley que considera poco razonable, no debería ser castigado',
    457: 'No creo que una persona deba beber nunca',
    458: 'Las personas que estaban cerca de mí cuando era niño (padre, padrastro, etc.) eran muy estrictas conmigo',
    459: 'Tengo varios malos hábitos tan arraigados que son difíciles de corregir',
    460: 'Sólo bebo un poco (o nada) con moderación',
    461: 'Me gustaría deshacerme de las preocupaciones causadas por mi boca rota',
    462: 'No creo que pueda contarle a la gente todo sobre mí',
    463: 'Antes me gustaba jugar a la rayuela',
    464: 'Nunca he tenido una visión',
    465: 'He cambiado de opinión varias veces sobre mi carrera de toda la vida',
    466: 'Nunca tomo medicamentos ni somníferos, salvo los que me indica mi médico',
    467: 'A menudo mimeografío números insignificantes (por ejemplo, matrículas de coches)',
    468: 'A menudo siento remordimientos porque pierdo los nervios y me quejo',
    469: 'Los rayos son una de las cosas que me dan miedo',
    470: 'Las cosas relacionadas con el sexo me dan asco',
    471: 'Mis profesores siempre me ponen malas notas en el colegio',
    472: 'El fuego me atrae', .
    473: 'Me gusta mantener a la gente adivinando mi próxima actividad',
    474: 'No orino más a menudo que los demás',
    475: 'Como último recurso, sólo revelo la parte de la verdad que no me perjudica',
    476: 'Soy un enviado especial de Dios',
    477: 'Si tengo el mismo defecto que algunos de mis amigos, prefiero soportarlo solo que involucrar a otros',
    478: 'Nunca me ha puesto especialmente nervioso que un miembro de mi familia se meta en problemas',
    479: 'El engaño mutuo de las personas es el único milagro que conozco',
    480: 'A menudo me da miedo la oscuridad',
    481: 'Me da miedo estar solo en la oscuridad',
    482: 'Mis planes parecen siempre tan difíciles que tengo que abandonarlos uno a uno',
    483: 'Dios (Dios) hace milagros',
    484: 'Hay algunos defectos que tengo que admitir e intentar controlar, pero que no puedo eliminar',
    485: 'Cuando un hombre está con una mujer, lo único en lo que suele pensar es en su aspecto sexual',
    486: 'Nunca he encontrado sangre en mi orina',
    487: 'A menudo me siento muy triste cuando intento evitar que la gente cometa errores y lo que hago se malinterpreta',
    488: 'Rezo varias veces a la semana',
    489: 'Me compadezco de los que no están libres de angustia y tristeza',
    490: 'Rezo el rosario varias veces por semana',
    491: 'Me impacientan los que piensan que sólo hay una religión verdadera en el mundo',
    492: 'Me asusto cuando pienso en terremotos',
    493: 'Me gusta el tipo de trabajo que requiere concentración y no el que requiere menos esfuerzo',
    494: 'Me da miedo estar encerrado en una habitación pequeña o en un lugar de confinamiento reducido',
    495: 'Siempre soy franco y comunicativo con aquellos a quienes quiero ayudar a corregir o mejorar',
    496: 'Nunca he visto una cosa como dos (el fenómeno de la visión doble)',
    497: 'Me gustan las novelas de aventuras',
    498: 'La franqueza siempre es buena',
    499: 'Debo admitir que a veces me preocupo sin razón por cosas que no tienen importancia',
    500: 'Estoy dispuesto a aceptar una buena opinión el 100% de las veces',
    501: 'Siempre he resuelto los problemas por mí mismo, en lugar de buscar a alguien que me diga lo que tengo que hacer',
    502: 'Las tormentas me dan pánico',
    503: 'No suelo expresar mi aprobación o desaprobación de las acciones de los demás',
    504: 'No quiero ocultar mis malas impresiones o simpatías sobre una persona para que no sepa lo que pienso de ella',
    505: 'Creo que 'al caballo que no tira del carro hay que azotarlo'',
    506: 'Soy una persona muy nerviosa',
    507: 'A menudo me encuentro con altos mandos que se atribuyen méritos y culpan de sus errores a sus subordinados',
    508: 'Creo que mi olfato es tan bueno como el de los demás',
    509: 'Como soy tan formal, a veces me resulta difícil hacer valer mi opinión',
    510: 'La suciedad me da miedo o me pone enfermo',
    511: 'Tengo una vida de ensueño que no quiero contar a nadie',
    512: 'No me gusta bañarme',
    513: 'Creo que es mejor buscar la felicidad de los demás que luchar por mi propia libertad',
    514: 'Me gustan las mujeres varoniles',
    515: 'Nuestra familia siempre se preocupa por la comida y la ropa',
    516: 'Algunas personas de mi familia tienen mal genio',
    517: 'No sé hacer nada bien',
    518: 'A menudo me avergüenzo porque no pienso y hago lo mismo sobre ciertas cosas',
    519: 'Tengo problemas con mis órganos sexuales',
    520: 'Siempre mantengo mis opiniones con firmeza',
    521: 'Suelo pedir consejo a los demás',
    522: 'No tengo miedo a las arañas',
    523: 'Nunca me ruborizo',
    524: 'No tengo miedo a contagiarme enfermedades de las manillas de las puertas',
    525: 'Algunos animales me ponen nervioso',
    526: 'Mi futuro no parece prometedor',
    527: 'Mi familia y parientes cercanos se llevan muy bien',
    528: 'No me sonrojo fácilmente en comparación con la gente',
    529: 'Me gusta llevar ropa elegante',
    530: 'A menudo me preocupa sonrojarme',
    531: 'Incluso cuando creo que he tomado una decisión sobre algo, es fácil que los demás me hagan cambiar de opinión o me hagan cambiar de opinión',
    532: 'Puedo soportar el mismo dolor que cualquier otra persona',
    533: 'No me molestan los hipos frecuentes',
    534: 'En varias ocasiones me he quedado solo para perseverar hasta el final antes de abandonar definitivamente lo que estaba haciendo',
    535: 'Tengo la boca seca casi todo el día',
    536: 'Me enfado cada vez que me meten prisa',
    537: 'Quiero ir a cazar tigres al bosque',
    538: 'Creo que me gustaría trabajar de sastre',
    539: 'No me dan miedo las ratas',
    540: 'Nunca se me ha paralizado la cara',
    541: 'Mi piel parece especialmente sensible al tacto',
    542: 'Nunca he tenido heces negras como el alquitrán',
    543: 'Unas cuantas veces a la semana tengo la sensación de que va a ocurrir algo terrible',
    544: 'Me siento cansado la mayor parte del tiempo',
    545: 'A veces tengo los mismos sueños una y otra vez',
    546: 'Me gusta leer libros de historia',
    547: 'El futuro es impredecible y es difícil hacer planes serios',
    548: 'Nunca iría a ver una película pornográfica si pudiera evitarlo',
    549: 'Muchas veces me siento indiferente ante cualquier cosa, aunque todo vaya bien',
    550: 'Me gusta arreglar las cerraduras de las puertas',
    551: 'A veces puedo estar seguro de que la gente sabe lo que pienso',
    552: 'Me gusta leer libros sobre ciencia',
    553: 'Me da miedo estar solo en un lugar abierto',
    554: 'Si fuera pintor, me gustaría dibujar niños',
    555: 'A veces siento que me voy a desmayar',
    556: 'Cuido mucho mi forma de vestir',
    557: 'Me gustaría ser secretaria personal',
    558: 'Mucha gente se avergüenza de haber tenido mal sexo',
    559: 'A menudo tengo miedo en mitad de la noche',
    560: 'A menudo me cuesta recordar dónde he puesto las cosas',
    561: 'Me gusta mucho montar a caballo',
    562: 'Cuando era niño, sentía más apego y admiración por una mujer (abuela, madre, hermana, tía, tío, etc.)',
    563: 'Me gustan más las novelas de aventuras que las románticas',
    564: 'No me enfado fácilmente',
    565: 'Cuando estoy en un lugar alto, tengo la tentación de saltar',
    566: 'Me gustan las escenas de amor en las películas'
}


# 用于存放测验的原始结果
# Used to store the original results of the questionnaire
Ans = {

}


def start():
    """
    Sección de la guía de preguntas con introducción y directrices
    Guide section, including abstract and instruction

    :return: None
    """
    print(Ins1)
    time.sleep(5)

    while 1:
        print('El cuestionario empezará a continuación, ¿empezamos? ')
        print('1. Sí    0. No')
        go = input('> ')
        if go == '1':
            print('-' * 65)
            print('El cuestionario comenzará oficialmente en 30 segundos, por favor lea y entienda lo siguiente cuidadosamente')
            time.sleep(3)
            print(Ins2)
            time.sleep(27)
            break
        elif go == '0':
            print('Gracias por utilizar este programa, ¡adiós!')
            time.sleep(3)
            exit(0)
        else:
            print('Si se ha equivocado, vuelva a introducir los datos tal y como exige el cuestionario.')
            continue


def answer():
    """for debug
    Preguntas y respuestas aleatorias
    random answer

    :return: '0' or '1'
    :rtype: str
    """
    ans = randint(0, 1)
    return str(ans)


def test():
    """
    Cuestionario
    test section

    :return: None
    """
    global Sex
    global Age

    print('El cuestionario ha comenzado oficialmente. ')
    print('-' * 65)
    time.sleep(3)

    while 1:
        print('x1. Mi género es')
        print('1. 男    0.女')
        Sex = input('> ')
        if Sex == '1' or Sex == '0':
            break
        else:
            print('输入错误请按照测验要求重新输入！')
            continue

    while 1:
        print('-' * 65)
        print('x2. 请输入你的年龄')
        Age = input('> ')

        if str.isdigit(Age):
            if 13 <= int(Age) <= 70:
                break
            else:
                print('本测验不适用于该年龄范围，感谢使用！')
                time.sleep(3)
                exit(0)
        else:
            print('输入错误请按照测验要求重新输入！')
            continue

    for i in range(len(Que)+1):
        if i == 73:
            if Sex == '1':
                temp_que = str(i+1) + '. ' + (Que[i+1][Que[i+1].find('m')+1: Que[i+1].find('f')])
            else:
                temp_que = str(i+1) + '. ' + (Que[i+1][Que[i+1].find('f') + 1:])
        elif i == len(Que):
            temp_que = str(len(Que)+1) + '.' + '我保证是在专业人士指导下认真诚实地完成本次测验'
        else:
            temp_que = str(i+1) + '. ' + Que[i+1]

        while 1:
            print('-' * 65)
            print(temp_que)
            print('1. 是    0. 否')
            temp_ans = input('> ')
            # temp_ans = answer()  # for debug
            # print('> ' + str(temp_ans))  # for debug
            if temp_ans == '1' or temp_ans == '0':
                Ans[i+1] = temp_ans
                # print(Ans)  # for debug
                break
            elif temp_ans == 'bomb':    # for debug
                exit(0)
            else:
                print('输入错误请按照测验要求重新输入！')
                continue

    print('-' * 65)
    print('测验结束，感谢您的配合！')
    print('-' * 65)


def is_diff(a, b):
    """
    为异计分
    Add point if different

    :param a: the first para
    :param b: the second para
    :return: 0 or 1

    :type a: str
    :type b: str
    :rtype: int
    """
    if a != b:
        return 1
    else:
        return 0


def is_true(t):
    """
    正向计分
    Add point if True

    :param t: the para under test
    :return: 0 or 1

    :type t: str
    :rtype: int
    """
    if t == '1':
        return 1
    else:
        return 0


def is_false(t):
    """
    反向计分
    Add point if False

    :param t: the para under test
    :return: 0 or 1

    :type t: str
    :rtype: 0 or 1
    """
    if t == '0':
        return 1
    else:
        return 0


def norm_select(sex):
    """
    选择常模表（中国1982版）
    the norm select (based on Chinese 1982's)

    :param sex: the subjects' sex
    :return: Norm_M, Norm_SD

    :type sex: str
    :rtype: None
    """
    global Norm_M
    global Norm_SD

    # 男性常模
    # male norm
    if sex == '1':
        Norm_M = {
            'L': 5.70,
            'F': 13.68,
            'K': 13.00,
            'Hs': 8.78,
            'D': 26.16,
            'Hy': 22.07,
            'Pd': 18.98,
            'Mf': 27.56,
            'Pa': 12.84,
            'Pt': 17.86,
            'Sc': 23.01,
            'Ma': 18.48,
            'Si': 34.51,
            'Hs+0.5K': 15.42,
            'Pd+0.4K': 24.38,
            'Pt+1.0K': 31.14,
            'Sc+1.0K': 36.47,
            'Ma+0.2K': 21.22,
            'Mas': 18.86,
            'Dy': 26.09,
            'Do': 15.39,
            'Re': 20.54,
            'Cn': 25.26
        }
        Norm_SD = {
            'L': 2.52,
            'F': 6.86,
            'K': 4.66,
            'Hs': 4.75,
            'D': 4.97,
            'Hy': 5.36,
            'Pd': 4.36,
            'Mf': 4.04,
            'Pa': 3.92,
            'Pt': 7.93,
            'Sc': 10.15,
            'Ma': 5.26,
            'Si': 6.88,
            'Hs+0.5K': 4.79,
            'Pd+0.4K': 4.27,
            'Pt+1.0K': 5.71,
            'Sc+1.0K': 8.24,
            'Ma+0.2K': 4.88,
            'Mas': 7.45,
            'Dy': 8.05,
            'Do': 3.12,
            'Re': 4.13,
            'Cn': 3.76
        }
    # 女性常模
    # female norm
    else:
        Norm_M = {
            'L': 5.64,
            'F': 11.69,
            'K': 12.25,
            'Hs': 9.83,
            'D': 28.40,
            'Hy': 22.82,
            'Pd': 18.29,
            'Mf': 31.83,
            'Pa': 12.62,
            'Pt': 18.77,
            'Sc': 22.50,
            'Ma': 16.64,
            'Si': 37.27,
            'Hs+0.5K': 16.35,
            'Pd+0.4K': 23.33,
            'Pt+1.0K': 31.17,
            'Sc+1.0K': 34.89,
            'Ma+0.2K': 19.18,
            'Mas': 20.43,
            'Dy': 29.12,
            'Do': 15.10,
            'Re': 21.78,
            'Cn': 24.86
        }
        Norm_SD = {
            'L': 2.48,
            'F': 5.02,
            'K': 4.26,
            'Hs': 4.98,
            'D': 5.04,
            'Hy': 5.54,
            'Pd': 4.45,
            'Mf': 3.86,
            'Pa': 3.93,
            'Pt': 7.82,
            'Sc': 9.57,
            'Ma': 5.16,
            'Si': 6.71,
            'Hs+0.5K': 4.95,
            'Pd+0.4K': 4.44,
            'Pt+1.0K': 5.86,
            'Sc+1.0K': 7.63,
            'Ma+0.2K': 4.89,
            'Mas': 7.35,
            'Dy': 7.61,
            'Do': 2.76,
            'Re': 3.13,
            'Cn': 3.70
        }



def trans_t(score, m, sd):
    """
    标准T分计算公式
    Standard T point conversion formula

    :param score: original score
    :param m: normative mean value
    :param sd: normative standard deviation
    :return: standard T score

    :type score: int
    :type m: float
    :type sd: float
    :rtype: int
    """
    t = round(50 + 10*(score - m)/sd)
    return t


def scale_q(ori_score=0, pro_score=0):
    """
    效度量表-疑问分数 Q
    the score of Q (? or question) scale,

    由于不允许被试者存在空题，故仅记录16项重复问题的矛盾数量
    because subjects were not allowed to have blank questions,
    just record the number of contradictions of 16 repeated questions

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    # 原始分 original score
    temp1 = [8, 13, 15, 16, 20, 21, 22, 23, 24, 32, 33, 35, 37, 38, 305, 317]
    temp2 = [318, 290, 314, 315, 310, 308, 326, 288, 333, 328, 323, 331, 302, 311, 366, 362]

    for i in range(len(temp1)):
        ori_score += is_diff(Ans[temp1[i]], Ans[temp2[i]])

    temp = ori_score
    pro_score += temp

    return ori_score, pro_score


def scale_l(ori_score=0, pro_score=0):
    """
    效度量表-说谎分数 L
    the score of L (lie) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    # 原始分 original score
    temp = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 195, 225, 255, 285]

    for i in temp:
        ori_score += is_false(Ans[i])

    pro_score += trans_t(ori_score, Norm_M['L'], Norm_SD['L'])

    return ori_score, pro_score


def scale_f(ori_score=0, pro_score=0):
    """
    效度量表-诈病分数 F
    the score of F (infrequency or fake bad) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    # 原始分 original score
    temp_t = [14, 27, 31, 34, 35, 40, 42, 48, 49, 50, 53, 56, 66, 85, 121, 123, 139, 146, 151, 156, 168, 184, 197, 200,
              202, 205, 206, 209, 210, 211, 215, 218, 227, 245, 246, 247, 252, 256, 269, 275, 286, 288, 291, 293]
    temp_f = [17, 20, 54, 65, 75, 83, 112, 113, 115, 164, 169, 177, 185, 196, 199, 220, 257, 258, 272, 276]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['F'], Norm_SD['F'])

    return ori_score, pro_score


def scale_k(ori_score=0, pro_score=0):
    """
    效度量表-校正分数 K
    the score of K (defensiveness) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [96]
    temp_f = [30, 39, 71, 89, 124, 129, 134, 138, 142, 148, 160, 170, 171, 180, 183, 217, 234, 267, 272, 296, 316, 322,
              368, 370, 372, 373, 375, 386, 394]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['K'], Norm_SD['K'])

    return ori_score, pro_score


def scale_hs(ori_score=0, pro_score=0, pro_score_add_k=0):
    """
    临床量表-1 疑病 Hs
    the score of Hs (hypochondriasis) scale

    :param ori_score: original score
    :param pro_score: processing score
    :param pro_score_add_k: processing score added 0.5K
    :return: ori_score, pro_score, pro_score_add_k

    :rtype: int, int, int
    """
    temp_t = [23, 29, 43, 62, 72, 108, 114, 125, 161, 189, 273]
    temp_f = [2, 3, 7, 9, 18, 51, 55, 63, 68, 103, 130, 153, 155, 163, 175, 188, 190, 192, 230, 243, 274, 281]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    k, ignore = scale_k()
    pro_score += trans_t(ori_score, Norm_M['Hs'], Norm_SD['Hs'])
    pro_score_add_k += trans_t(ori_score + round(0.5 * k), Norm_M['Hs+0.5K'], Norm_SD['Hs+0.5K'])

    return ori_score, pro_score, pro_score_add_k


def scale_d(ori_score=0, pro_score=0):
    """
    临床量表-2 抑郁 D
    the score of D (depression) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [5, 32, 41, 43, 52, 67, 86, 104, 130, 138, 142, 158, 159, 182, 189, 193, 236, 259, 288, 290]
    temp_f = [2, 8, 9, 18, 30, 36, 39, 46, 51, 57, 58, 64, 80, 88, 89, 95, 98, 107, 122, 131, 145, 152, 153, 154, 155,
              160, 178, 191, 207, 208, 233, 241, 242, 248, 263, 270, 271, 272, 285, 296]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['D'], Norm_SD['D'])

    return ori_score, pro_score


def scale_hy(ori_score=0, pro_score=0):
    """
    临床量表-3 癔病 Hy
    the score of Hy (hysteria) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [10, 23, 32, 43, 44, 47, 76, 114, 179, 186, 189, 238, 253]
    temp_f = [2, 3, 6, 7, 8, 9, 12, 26, 30, 51, 55, 71, 89, 93, 103, 107, 109, 124, 128, 129, 136, 137, 141, 147, 153,
              160, 162, 163, 170, 172, 174, 175, 180, 188, 190, 192, 201, 213, 230, 234, 243, 265, 267, 274, 279, 289,
              292]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Hy'], Norm_SD['Hy'])

    return ori_score, pro_score


def scale_pd(ori_score=0, pro_score=0, pro_score_add_k=0):
    """
    临床量表-4 精神病态 Pd
    the score of Pd (psychopathic deviate) scale

    :param ori_score: original score
    :param pro_score: processing score
    :param pro_score_add_k: processing score added 0.4K
    :return: ori_score, pro_score, pro_score_add_k

    :rtype: int, int, int
    """
    temp_t = [16, 21, 24, 32, 33, 35, 38, 42, 61, 67, 84, 94, 102, 106, 110, 118, 127, 215, 216, 224, 239, 244, 245,
              284]
    temp_f = [8, 20, 37, 82, 91, 96, 107, 134, 137, 141, 155, 170, 171, 173, 180, 183, 201, 231, 235, 237, 248, 267,
              287, 289, 294, 296]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    k, ignore = scale_k()
    pro_score += trans_t(ori_score, Norm_M['Pd'], Norm_SD['Pd'])
    pro_score_add_k += trans_t(ori_score + round(0.4 * k), Norm_M['Pd+0.4K'], Norm_SD['Pd+0.4K'])

    return ori_score, pro_score, pro_score_add_k


def scale_mf(ori_score=0, pro_score=0):
    """
    临床量表-5 男子气/女子气 Mf
    the score of Mf (masculinity-femininity) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    # 男性女性化 Mf-m
    if Sex == '1':
        temp_t = [4, 25, 69, 70, 74, 77, 78, 87, 92, 126, 132, 134, 140, 149, 179, 187, 203, 204, 217, 226, 231, 239,
                  261, 278, 282, 295, 297, 299]
        temp_f = [1, 19, 26, 28, 79, 80, 81, 89, 99, 112, 115, 116, 117, 120, 133, 144, 176, 198, 213, 214, 219, 221,
                  223, 229, 249, 254, 260, 262, 264, 280, 283, 300]
    # 女性男性化 Mf-f
    else:
        temp_t = [4, 25, 70, 74, 77, 78, 87, 92, 126, 132, 133, 134, 140, 149, 187, 203, 204, 217, 226, 239, 261, 278,
                  282, 295, 299]
        temp_f = [1, 19, 26, 28, 69, 79, 80, 81, 89, 99, 112, 115, 116, 117, 120, 144, 176, 179, 198, 213, 214, 219,
                  221, 223, 229, 231, 249, 254, 260, 262, 264, 280, 283, 297, 300]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Mf'], Norm_SD['Mf'])

    return ori_score, pro_score


def scale_pa(ori_score=0, pro_score=0):
    """
    临床量表-6 妄想狂 Pa
    the score of Pa (paranoia) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [16, 24, 27, 35, 110, 121, 123, 127, 151, 157, 158, 202, 275, 284, 291, 293, 299, 305, 314, 317, 326, 338,
              341, 364, 365]
    temp_f = [93, 107, 109, 111, 117, 124, 268, 281, 294, 313, 316, 319, 327, 347, 348]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Pa'], Norm_SD['Pa'])

    return ori_score, pro_score


def scale_pt(ori_score=0, pro_score=0, pro_score_add_k=0):
    """
    临床量表-7 精神衰弱 Pt
    the score of Pt (psychasthenia) scale

    :param ori_score: original score
    :param pro_score: processing score
    :param pro_score_add_k: processing score added 1.0K
    :return: ori_score, pro_score, pro_score_add_k

    :rtype: int, int, int
    """
    temp_t = [10, 15, 22, 32, 41, 67, 76, 86, 94, 102, 106, 142, 159, 182, 189, 217, 238, 266, 301, 304, 321, 336, 337,
              340, 342, 343, 344, 346, 349, 351, 352, 356, 357, 358, 359, 360, 361, 362, 366]
    temp_f = [3, 8, 36, 122, 152, 164, 178, 329, 353]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    k, ignore = scale_k()
    pro_score += trans_t(ori_score, Norm_M['Pt'], Norm_SD['Pt'])
    pro_score_add_k += trans_t(ori_score + k, Norm_M['Pt+1.0K'], Norm_SD['Pt+1.0K'])

    return ori_score, pro_score, pro_score_add_k


def scale_sc(ori_score=0, pro_score=0, pro_score_add_k=0):
    """
    临床量表-8 精神分裂症 Sc
    the score of Sc (schizophrenia) scale

    :param ori_score: original score
    :param pro_score: processing score
    :param pro_score_add_k: processing score added 1.0K
    :return: ori_score, pro_score, pro_score_add_k

    :rtype: int, int, int
    """
    temp_t = [15, 22, 40, 41, 47, 52, 76, 97, 104, 121, 156, 157, 159, 168, 179, 182, 194, 202, 210, 212, 238, 241, 251,
              259, 266, 273, 282, 291, 297, 301, 303, 307, 308, 311, 312, 315, 320, 323, 324, 325, 328, 331, 332, 333,
              334, 335, 339, 341, 345, 349, 350, 352, 354, 355, 356, 360, 363, 364, 366]
    temp_f = [17, 65, 103, 119, 177, 178, 187, 192, 196, 220, 276, 281, 302, 306, 309, 310, 318, 322, 330]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    k, ignore = scale_k()
    pro_score += trans_t(ori_score, Norm_M['Sc'], Norm_SD['Sc'])
    pro_score_add_k += trans_t(ori_score + k, Norm_M['Sc+1.0K'], Norm_SD['Sc+1.0K'])

    return ori_score, pro_score, pro_score_add_k


def scale_ma(ori_score=0, pro_score=0, pro_score_add_k=0):
    """
    临床量表-9 轻躁狂 Ma
    the score of Ma (hypomania) scale

    :param ori_score: original score
    :param pro_score: processing score
    :param pro_score_add_k: processing score added 0.2K
    :return: ori_score, pro_score, pro_score_add_k

    :rtype: int, int, int
    """
    temp_t = [11, 13, 21, 22, 59, 64, 73, 97, 100, 109, 127, 134, 143, 156, 157, 167, 181, 194, 212, 222, 226, 228, 232,
              233, 238, 240, 250, 251, 263, 266, 268, 271, 277, 279, 298]
    temp_f = [101, 105, 111, 119, 120, 148, 166, 171, 180, 267, 289]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    k, ignore = scale_k()
    pro_score += trans_t(ori_score, Norm_M['Ma'], Norm_SD['Ma'])
    pro_score_add_k += trans_t(ori_score + round(0.2 * k), Norm_M['Ma+0.2K'], Norm_SD['Ma+0.2K'])

    return ori_score, pro_score, pro_score_add_k


def scale_si(ori_score=0, pro_score=0):
    """
    临床量表-0 社会内向性 Si
    the score of Si (social introversion) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [32, 67, 82, 111, 117, 124, 138, 147, 171, 172, 180, 201, 236, 267, 278, 292, 304, 316, 321, 332, 336, 342,
              357, 369, 370, 373, 376, 378, 379, 385, 389, 393, 398, 399]
    temp_f = [25, 33, 57, 91, 99, 110, 126, 143, 193, 208, 229, 231, 254, 262, 281, 296, 309, 353, 359, 367, 371, 374,
              377, 380, 381, 382, 383, 384, 387, 388, 390, 391, 392, 395, 396, 397]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Si'], Norm_SD['Si'])

    return ori_score, pro_score


def scale_mas(ori_score=0, pro_score=0):
    """
    附加量表- 外显性焦虑 Mas
    the score of Mas (Manifest anxiety) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [13, 14, 23, 31, 32, 43, 67, 86, 125, 142, 158, 186, 191, 217, 238, 241, 263, 301, 317, 321, 322, 335, 337,
              340, 352, 361, 372, 398, 418, 424, 431, 439, 442, 499, 506, 530, 555]
    temp_f = [7, 18, 107, 163, 190, 230, 242, 264, 287, 367, 407, 520, 528]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Mas'], Norm_SD['Mas'])

    return ori_score, pro_score


def scale_dy(ori_score=0, pro_score=0):
    """
    附加量表- 依赖性 Dy
    the score of Dy (Dependency) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [19, 21, 24, 41, 63, 67, 70, 82, 86, 98, 100, 138, 141, 158, 165, 180, 189, 201, 212, 236, 239, 259, 267,
              304, 305, 321, 337, 338, 343, 357, 361, 362, 370, 372, 373, 393, 398, 399, 408, 440, 443, 461, 487, 488,
              489, 509, 521, 531, 554]
    temp_f = [9, 79, 107, 163, 170, 193, 264, 411]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Dy'], Norm_SD['Dy'])

    return ori_score, pro_score


def scale_do(ori_score=0, pro_score=0):
    """
    附加量表- 支配性 Do
    the score of Do (Dominance) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [64, 229, 255, 270, 406, 432, 523]
    temp_f = [32, 61, 82, 86, 94, 186, 223, 224, 240, 249, 250, 267, 268, 304, 343, 356, 419, 483, 547, 558, 562]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Do'], Norm_SD['Do'])

    return ori_score, pro_score


def scale_re(ori_score=0, pro_score=0):
    """
    附加量表- 社会责任感 Re
    the score of Re (Social Responsibility) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [58, 111, 173, 221, 294, 412, 501, 552]
    temp_f = [6, 28, 30, 33, 56, 116, 118, 157, 175, 181, 223, 224, 260, 304, 388, 419, 434, 437, 468, 471, 472, 529,
              553, 558]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Re'], Norm_SD['Re'])

    return ori_score, pro_score


def scale_cn(ori_score=0, pro_score=0):
    """
    附加量表- 控制 Cn
    the score of Cn (Control) scale

    :param ori_score: original score
    :param pro_score: processing score
    :return: ori_score, pro_score

    :rtype: int, int
    """
    temp_t = [6, 20, 30, 56, 67, 105, 116, 134, 145, 162, 169, 181, 225, 236, 238, 285, 296, 319, 337, 376, 379, 381,
              418, 447, 460, 461, 529, 555]
    temp_f = [58, 80, 92, 96, 111, 167, 174, 220, 242, 249, 250, 291, 313, 360, 439, 444, 449, 483, 488, 489, 527, 548]

    for i in temp_t:
        ori_score += is_true(Ans[i])
    for j in temp_f:
        ori_score += is_false(Ans[j])

    pro_score += trans_t(ori_score, Norm_M['Cn'], Norm_SD['Cn'])

    return ori_score, pro_score


def calculate_score():
    """
    测验分数计算
    calculate the score

    :return: None
    """
    global ori_Point
    global pro_Point

    ori_Point = {

    }
    pro_Point = {

    }

    norm_select(Sex)

    ori_Point['Q*'], pro_Point['Q*'] = scale_q()
    ori_Point['L'], pro_Point['L'] = scale_l()
    ori_Point['F'], pro_Point['F'] = scale_f()
    ori_Point['K'], pro_Point['K'] = scale_k()
    ori_Point['Hs'], pro_Point['Hs'], pro_Point['Hs+0.5K'] = scale_hs()
    ori_Point['D'], pro_Point['D'] = scale_d()
    ori_Point['Hy'], pro_Point['Hy'] = scale_hy()
    ori_Point['Pd'], pro_Point['Pd'], pro_Point['Pd+0.4K'] = scale_pd()
    ori_Point['Mf'], pro_Point['Mf'] = scale_mf()
    ori_Point['Pa'], pro_Point['Pa'] = scale_pa()
    ori_Point['Pt'], pro_Point['Pt'], pro_Point['Pt+1.0K'] = scale_pt()
    ori_Point['Sc'], pro_Point['Sc'], pro_Point['Sc+1.0K'] = scale_sc()
    ori_Point['Ma'], pro_Point['Ma'], pro_Point['Ma+0.2K'] = scale_ma()
    ori_Point['Si'], pro_Point['Si'] = scale_si()
    ori_Point['Mas'], pro_Point['Mas'] = scale_mas()
    ori_Point['Dy'], pro_Point['Dy'] = scale_dy()
    ori_Point['Do'], pro_Point['Do'] = scale_do()
    ori_Point['Re'], pro_Point['Re'] = scale_re()
    ori_Point['Cn'], pro_Point['Cn'] = scale_cn()


def analyze_score():
    """
    分析测验分数
    analyze the score of test

    利用两点编码法以及剖析图方式呈现被测者的人格特点
    Use 2 point codes and personality profile to show the personality traits of the subjects

    :return:None
    """
    global two_point

    val_scale = ['L', 'F', 'K']
    cli_scale = ['Hs\n1', 'D\n2', 'Hy\n3', 'Pd\n4', 'Mf\n5', 'Pa\n6', 'Pt\n7', 'Sc\n8', 'Ma\n9', 'Si\n0']
    ext_scale = ['Mas', 'Dy', 'Do', 'Re', 'Cn']

    val_list = [
        pro_Point['L'],
        pro_Point['F'],
        pro_Point['K']
    ]
    cli_list = [
        pro_Point['Hs+0.5K'],
        pro_Point['D'],
        pro_Point['Hy'],
        pro_Point['Pd+0.4K'],
        pro_Point['Mf'],
        pro_Point['Pa'],
        pro_Point['Pt+1.0K'],
        pro_Point['Sc+1.0K'],
        pro_Point['Ma+0.2K'],
        pro_Point['Si']
    ]
    ext_list = [
        pro_Point['Mas'],
        pro_Point['Dy'],
        pro_Point['Do'],
        pro_Point['Re'],
        pro_Point['Cn']
    ]

    cli_max1 = max(cli_list)
    cli_max1_index = cli_list.index(cli_max1)
    if cli_max1_index != 9:
        first = cli_max1_index + 1
    else:
        first = 0
    cli_list[cli_max1_index] = 0
    cli_max2 = max(cli_list)
    cli_max2_index = cli_list.index(cli_max2)
    if cli_max2_index != 9:
        second = cli_max2_index + 1
    else:
        second = 0
    cli_list[cli_max1_index] = cli_max1
    two_point = '%s%s' % (str(first), str(second))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=(10, 6), dpi=100, linewidth=1)
    ax = fig.add_subplot(111)
    ax.plot(range(len(val_list)), val_list, 'b*-')
    ax.plot(range(len(val_list), len(val_list) + len(cli_list)), cli_list, 'b*-')
    ax.plot(range(len(val_list) + len(cli_list), len(val_list) + len(cli_list) + len(ext_list)), ext_list, 'b*-')
    # plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45)
    ax.set_xticks(range(len(val_list + cli_list + ext_list)))
    ax.set_xticklabels(val_scale + cli_scale + ext_scale)
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
    ax.set_xlim(-0.5, len(val_scale + cli_scale + ext_scale) - 0.5)
    ax.set_ylim(0, 120)
    plt.axvline(2.5, ls="-", color="black")
    plt.axvline(12.5, ls="-", color="black")
    plt.axvline(7, ls="--", color="red")
    plt.axhline(50, ls="-", color="black")
    plt.axhline(60, ls="--", color="black")
    plt.axhline(70, ls="-", color="black")
    ax.plot(cli_max1_index + len(val_list), cli_max1, 'rp')
    ax.plot(cli_max2_index + len(val_list), cli_max2, 'rp')
    plt.annotate(r'$max1$', xy=(cli_max1_index + len(val_list)+0.1, cli_max1+2), color='red', fontsize=8)
    plt.annotate(r'$max2$', xy=(cli_max2_index + len(val_list)+0.1, cli_max2+2), color='red', fontsize=8)


def data_export():
    """
    导出数据
    export test data

    :return: None

    Note: Generate a '.xlsx' file to save the test information
    """
    print('请输入被试者姓名')
    name = input('> ')
    wb = Workbook()
    data_filename = time.strftime("%Y%m%d_%H%M_", time.localtime()) + name + '_MMPI测验'

    font1 = Font(name='黑体', size=12)
    font2 = Font(name='宋体', size=12)
    font3 = Font(name='Times New Roman', size=12, bold=True)
    font4 = Font(name='Times New Roman', size=12)
    alig1 = Alignment(horizontal='center', vertical='center')
    alig2 = Alignment(horizontal='general', vertical='center')

    # 表1，记录测验原始数据
    sheet1 = wb.active
    sheet1.title = '测验原始数据'
    sheet1['A1'] = '姓名'
    sheet1['A1'].font = font1
    sheet1['A1'].alignment = alig1
    sheet1['C1'] = '性别'
    sheet1['C1'].font = font1
    sheet1['C1'].alignment = alig1
    sheet1['E1'] = '年龄'
    sheet1['E1'].font = font1
    sheet1['E1'].alignment = alig1
    sheet1.merge_cells('A2:B2')
    sheet1['A2'] = '题 目'
    sheet1['A2'].font = font1
    sheet1['A2'].alignment = alig1
    sheet1.merge_cells('C2:D2')
    sheet1['C2'] = '回 答'
    sheet1['C2'].font = font1
    sheet1['C2'].alignment = alig1
    sheet1['B1'] = name
    sheet1['B1'].font = font2
    sheet1['B1'].alignment = alig1
    if Sex == '1':
        sex_name = '男'
    else:
        sex_name = '女'
    sheet1['D1'] = sex_name
    sheet1['D1'].font = font2
    sheet1['D1'].alignment = alig1
    sheet1['F1'] = Age
    sheet1['F1'].font = font4
    sheet1['F1'].alignment = alig1
    for i in range(len(Que)+1):
        if i == 73:
            if Sex == '1':
                temp_que = Que[i+1][Que[i+1].find('m')+1: Que[i+1].find('f')]
            else:
                temp_que = Que[i+1][Que[i+1].find('f') + 1:]
        elif i == len(Que):
            temp_que = '我保证是在专业人士指导下认真诚实地完成本次测验'
        else:
            temp_que = Que[i+1]

        sheet1['A%d' % (i + 3)].value = str(i + 1) + '.'
        sheet1['A%d' % (i + 3)].font = font2
        sheet1['A%d' % (i + 3)].alignment = alig1
        sheet1['B%d' % (i + 3)].value = temp_que
        sheet1['B%d' % (i + 3)].font = font2
        sheet1['B%d' % (i + 3)].alignment = alig2
        if Ans[i+1] == '1':
            temp_ans = '是'
            sheet1['C%d' % (i + 3)].value = temp_ans
            sheet1['C%d' % (i + 3)].font = font2
            sheet1['C%d' % (i + 3)].alignment = alig1
        else:
            temp_ans = '否'
            sheet1['D%d' % (i + 3)].value = temp_ans
            sheet1['D%d' % (i + 3)].font = font2
            sheet1['D%d' % (i + 3)].alignment = alig1

    # 表2，记录测验分数
    sheet2 = wb.create_sheet(title='测验分数')
    sheet2['A1'] = '姓名'
    sheet2['A1'].font = font1
    sheet2['A1'].alignment = alig1
    sheet2['C1'] = '性别'
    sheet2['C1'].font = font1
    sheet2['C1'].alignment = alig1
    sheet2['E1'] = '年龄'
    sheet2['E1'].font = font1
    sheet2['E1'].alignment = alig1
    sheet2['B1'].value = name
    sheet2['B1'].font = font2
    sheet2['B1'].alignment = alig1
    sheet2['D1'].value = sex_name
    sheet2['D1'].font = font2
    sheet2['D1'].alignment = alig1
    sheet2['F1'].value = Age
    sheet2['F1'].font = font4
    sheet2['F1'].alignment = alig1
    sheet2['A2'] = '量表类别'
    sheet2['A2'].font = font1
    sheet2['A2'].alignment = alig1
    sheet2['B2'] = '原始分'
    sheet2['B2'].font = font1
    sheet2['B2'].alignment = alig1
    sheet2['C2'] = '标准分（不加K）'
    sheet2['C2'].font = font1
    sheet2['C2'].alignment = alig1
    sheet2['D2'] = '标准分（加K）'
    sheet2['D2'].font = font1
    sheet2['D2'].alignment = alig1
    sheet2['A3'] = '*其中Q量表仅记录矛盾题的数量'
    sheet2['A3'].font = font2
    sheet2['A3'].alignment = alig2
    scale_list = ['Q*', 'L', 'F', 'K', 'Hs', 'D', 'Hy', 'Pd', 'Mf', 'Pa', 'Pt', 'Sc', 'Ma', 'Si',
                  'Mas', 'Dy', 'Do', 'Re', 'Cn']
    for i in range(len(scale_list)):
        sheet2['A%d' % (i+4)].value = scale_list[i]
        sheet2['A%d' % (i+4)].font = font3
        sheet2['A%d' % (i+4)].alignment = alig1
        sheet2['B%d' % (i+4)].value = ori_Point[scale_list[i]]
        sheet2['B%d' % (i+4)].font = font4
        sheet2['B%d' % (i+4)].alignment = alig1
        sheet2['C%d' % (i+4)].value = pro_Point[scale_list[i]]
        sheet2['C%d' % (i+4)].font = font4
        sheet2['C%d' % (i+4)].alignment = alig1
        if scale_list[i] == 'Hs':
            sheet2['D%d' % (i + 4)].value = pro_Point['Hs+0.5K']
            sheet2['D%d' % (i + 4)].font = font4
            sheet2['D%d' % (i + 4)].alignment = alig1
        elif scale_list[i] == 'Pd':
            sheet2['D%d' % (i + 4)].value = pro_Point['Pd+0.4K']
            sheet2['D%d' % (i + 4)].font = font4
            sheet2['D%d' % (i + 4)].alignment = alig1
        elif scale_list[i] == 'Pt':
            sheet2['D%d' % (i + 4)].value = pro_Point['Pt+1.0K']
            sheet2['D%d' % (i + 4)].font = font4
            sheet2['D%d' % (i + 4)].alignment = alig1
        elif scale_list[i] == 'Sc':
            sheet2['D%d' % (i + 4)].value = pro_Point['Sc+1.0K']
            sheet2['D%d' % (i + 4)].font = font4
            sheet2['D%d' % (i + 4)].alignment = alig1
        elif scale_list[i] == 'Ma':
            sheet2['D%d' % (i + 4)].value = pro_Point['Ma+0.2K']
            sheet2['D%d' % (i + 4)].font = font4
            sheet2['D%d' % (i + 4)].alignment = alig1
        else:
            pass
    sheet2['E2'] = '两点编码'
    sheet2['E2'].font = font1
    sheet2['E2'].alignment = alig1
    sheet2['F2'].value = two_point
    sheet2['F2'].font = font4
    sheet2['F2'].alignment = alig1

    wb.save(filename=data_filename + '.xlsx')
    plt.title('%s MMPI剖析图 加K分校正T分（中国常模）' % name)
    plt.savefig(data_filename)
