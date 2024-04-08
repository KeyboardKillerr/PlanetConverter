from converter import *


async def main():
    logger = AsyncConsoleLogger()

    filesys = FileSys('C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zs\\Input',
                      'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zs\\Output',
                      None,
                      'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\ChangeName_ZapSib.csv',
                      'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_exp = FileSys('C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zs\\Input',
                          'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zs\\Output_exp',
                          None,
                          None,
                          'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_b = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Бурятское УГМС\\Input',
                        'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\b\\Output',
                        None,
                        'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\ChangeName_ZapSib.csv',
                        'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_b_exp = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Бурятское УГМС\\Input',
                            'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\b\\Output',
                            None,
                            None,
                            'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_zb = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Забайкальское УГМС\\Input',
                         'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zb\\Output',
                         None,
                         'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\ChangeName_ZapSib.csv',
                         'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_zb_exp = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Забайкальское УГМС\\Input',
                             'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\zb\\Output',
                             None,
                             None,
                             'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_i = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Иркутское УГМС\\Input',
                        'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\i\\Output',
                        None,
                        'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\ChangeName_ZapSib.csv',
                        'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_i_exp = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Иркутское УГМС\\Input',
                            'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\i\\Output',
                            None,
                            None,
                            'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_oi = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Обь-Иртышское УГМС\\Input',
                         'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\oi\\Output',
                         None,
                         None,
                         'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    filesys_oi_exp = FileSys('C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Обь-Иртышское УГМС\\Input',
                             'C:\\Users\\radia\\PycharmProjects\\pythonProject\\tests\\test_files\\oi\\Output',
                             None,
                             None,
                             'C:\\Users\\radia\\OneDrive\\Рабочий стол\\Планета\\Гидропосты_правл_Зап_Сиб\\Гидропосты.shp')

    converter_app_zs = ConverterApp(filesys, '-', logger, ParserZS)
    converter_app_zs_exp = ConverterApp(filesys_exp, '-', logger, ParserZS)
    converter_app_b = ConverterApp(filesys_b, '-', logger, ParserB)
    converter_app_b_exp = ConverterApp(filesys_b_exp, '-', logger, ParserB)
    converter_app_zb = ConverterApp(filesys_zb, '-', logger, ParserZB)
    converter_app_zb_exp = ConverterApp(filesys_zb_exp, '-', logger, ParserZB)
    converter_app_i = ConverterApp(filesys_i, '-', logger, ParserI)
    converter_app_i_exp = ConverterApp(filesys_i_exp, '-', logger, ParserI)
    converter_app_oi = ConverterApp(filesys_oi, '-', logger, ParserOI)
    converter_app_oi_exp = ConverterApp(filesys_oi_exp, '-', logger, ParserOI)

    # await converter_app_zs.convert_async()
    # await converter_app_zs_exp.convert_async()
    # await converter_app_b.convert_async()
    # await converter_app_b_exp.convert_async()
    await converter_app_zb.convert_async()
    await converter_app_zb_exp.convert_async()
    # await converter_app_i.convert_async()
    # await converter_app_i_exp.convert_async()
    # await converter_app_oi.convert_async()
    # await converter_app_oi_exp.convert_async()


if __name__ == "__main__":
    asyncio.run(main())
