"""The namespace contains the XMP Basic Schema related helper classes, constants and methods that provide basic descriptive information."""
from typing import List, Optional, Dict, Iterable
import enum
import aspose.pycore
import aspose.pydrawing
import aspose.imaging
import aspose.imaging.apsbuilder
import aspose.imaging.apsbuilder.dib
import aspose.imaging.asynctask
import aspose.imaging.brushes
import aspose.imaging.dithering
import aspose.imaging.exif
import aspose.imaging.exif.enums
import aspose.imaging.extensions
import aspose.imaging.fileformats
import aspose.imaging.fileformats.apng
import aspose.imaging.fileformats.avif
import aspose.imaging.fileformats.bigtiff
import aspose.imaging.fileformats.bmp
import aspose.imaging.fileformats.bmp.structures
import aspose.imaging.fileformats.cdr
import aspose.imaging.fileformats.cdr.const
import aspose.imaging.fileformats.cdr.enum
import aspose.imaging.fileformats.cdr.objects
import aspose.imaging.fileformats.cdr.types
import aspose.imaging.fileformats.cmx
import aspose.imaging.fileformats.cmx.objectmodel
import aspose.imaging.fileformats.cmx.objectmodel.enums
import aspose.imaging.fileformats.cmx.objectmodel.specs
import aspose.imaging.fileformats.cmx.objectmodel.styles
import aspose.imaging.fileformats.core
import aspose.imaging.fileformats.core.vectorpaths
import aspose.imaging.fileformats.dicom
import aspose.imaging.fileformats.djvu
import aspose.imaging.fileformats.dng
import aspose.imaging.fileformats.dng.decoder
import aspose.imaging.fileformats.emf
import aspose.imaging.fileformats.emf.dtyp
import aspose.imaging.fileformats.emf.dtyp.commondatastructures
import aspose.imaging.fileformats.emf.emf
import aspose.imaging.fileformats.emf.emf.consts
import aspose.imaging.fileformats.emf.emf.objects
import aspose.imaging.fileformats.emf.emf.records
import aspose.imaging.fileformats.emf.emfplus
import aspose.imaging.fileformats.emf.emfplus.consts
import aspose.imaging.fileformats.emf.emfplus.objects
import aspose.imaging.fileformats.emf.emfplus.records
import aspose.imaging.fileformats.emf.emfspool
import aspose.imaging.fileformats.emf.emfspool.records
import aspose.imaging.fileformats.emf.graphics
import aspose.imaging.fileformats.eps
import aspose.imaging.fileformats.eps.consts
import aspose.imaging.fileformats.gif
import aspose.imaging.fileformats.gif.blocks
import aspose.imaging.fileformats.ico
import aspose.imaging.fileformats.jpeg
import aspose.imaging.fileformats.jpeg2000
import aspose.imaging.fileformats.opendocument
import aspose.imaging.fileformats.opendocument.enums
import aspose.imaging.fileformats.opendocument.objects
import aspose.imaging.fileformats.opendocument.objects.brush
import aspose.imaging.fileformats.opendocument.objects.font
import aspose.imaging.fileformats.opendocument.objects.graphic
import aspose.imaging.fileformats.opendocument.objects.pen
import aspose.imaging.fileformats.pdf
import aspose.imaging.fileformats.png
import aspose.imaging.fileformats.psd
import aspose.imaging.fileformats.svg
import aspose.imaging.fileformats.svg.graphics
import aspose.imaging.fileformats.tga
import aspose.imaging.fileformats.tiff
import aspose.imaging.fileformats.tiff.enums
import aspose.imaging.fileformats.tiff.filemanagement
import aspose.imaging.fileformats.tiff.filemanagement.bigtiff
import aspose.imaging.fileformats.tiff.instancefactory
import aspose.imaging.fileformats.tiff.pathresources
import aspose.imaging.fileformats.tiff.tifftagtypes
import aspose.imaging.fileformats.webp
import aspose.imaging.fileformats.wmf
import aspose.imaging.fileformats.wmf.consts
import aspose.imaging.fileformats.wmf.graphics
import aspose.imaging.fileformats.wmf.objects
import aspose.imaging.fileformats.wmf.objects.escaperecords
import aspose.imaging.imagefilters
import aspose.imaging.imagefilters.complexutils
import aspose.imaging.imagefilters.convolution
import aspose.imaging.imagefilters.filteroptions
import aspose.imaging.imageloadoptions
import aspose.imaging.imageoptions
import aspose.imaging.interfaces
import aspose.imaging.magicwand
import aspose.imaging.magicwand.imagemasks
import aspose.imaging.masking
import aspose.imaging.masking.options
import aspose.imaging.masking.result
import aspose.imaging.memorymanagement
import aspose.imaging.multithreading
import aspose.imaging.palettehelper
import aspose.imaging.progressmanagement
import aspose.imaging.shapes
import aspose.imaging.shapesegments
import aspose.imaging.sources
import aspose.imaging.watermark
import aspose.imaging.watermark.options
import aspose.imaging.xmp
import aspose.imaging.xmp.schemas
import aspose.imaging.xmp.schemas.dicom
import aspose.imaging.xmp.schemas.dublincore
import aspose.imaging.xmp.schemas.pdf
import aspose.imaging.xmp.schemas.photoshop
import aspose.imaging.xmp.schemas.xmpbaseschema
import aspose.imaging.xmp.schemas.xmpdm
import aspose.imaging.xmp.schemas.xmpmm
import aspose.imaging.xmp.schemas.xmprm
import aspose.imaging.xmp.types
import aspose.imaging.xmp.types.basic
import aspose.imaging.xmp.types.complex
import aspose.imaging.xmp.types.complex.colorant
import aspose.imaging.xmp.types.complex.dimensions
import aspose.imaging.xmp.types.complex.font
import aspose.imaging.xmp.types.complex.resourceevent
import aspose.imaging.xmp.types.complex.resourceref
import aspose.imaging.xmp.types.complex.thumbnail
import aspose.imaging.xmp.types.complex.version
import aspose.imaging.xmp.types.derived

class XmpBasicPackage(aspose.imaging.xmp.XmpPackage):
    '''Represents XMP basic namespace.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, prefix: str, namespace_uri: str):
        '''Initializes a new instance of the  class.
        
        :param prefix: The prefix.
        :param namespace_uri: The namespace URI.'''
        ...
    
    @overload
    def set_created_date(self, created_date: DateTime):
        '''Adds resource created date.
        
        :param created_date: Created date.'''
        ...
    
    @overload
    def set_created_date(self, created_date: str):
        '''Adds resource created date.
        
        :param created_date: Created date.'''
        ...
    
    @overload
    def set_metadata_date(self, metadata_date: DateTime):
        '''Adds metadata last changed date.
        
        :param metadata_date: Metadata date.'''
        ...
    
    @overload
    def set_metadata_date(self, metadata_date: str):
        '''Adds metadata last changed date.
        
        :param metadata_date: Metadata date.'''
        ...
    
    @overload
    def set_modify_date(self, modified_date: DateTime):
        '''Adds resource last modified date.
        
        :param modified_date: Last modified date.'''
        ...
    
    @overload
    def set_modify_date(self, modified_date: str):
        '''Adds resource last modified date.
        
        :param modified_date: Last modified date.'''
        ...
    
    def contains_key(self, key: str) -> bool:
        '''Determines whether the specified key contains key.
        
        :param key: The key to be checked.
        :returns: Returns true if the specified key contains key.'''
        ...
    
    def get_prop_value(self, key: str) -> any:
        '''Gets the  with the specified key.
        
        :param key: The key that identifies value.
        :returns: Returns the  with the specified key.'''
        ...
    
    def set_prop_value(self, key: str, value: any):
        '''Gets or sets the  with the specified key.
        
        :param key: The key that identifies value.
        :param value: The  with the specified key.'''
        ...
    
    def add_value(self, key: str, value: str):
        '''Adds string property.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The string value.'''
        ...
    
    def remove(self, key: str) -> bool:
        '''Remove the value with the specified key.
        
        :param key: The string representation of key that is identified with removed value.
        :returns: Returns true if the value with the specified key was removed.'''
        ...
    
    def clear(self):
        '''Clears this instance.'''
        ...
    
    def set_value(self, key: str, value: aspose.imaging.xmp.IXmlValue):
        '''Sets the value.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        ...
    
    def set_xmp_type_value(self, key: str, value: aspose.imaging.xmp.types.XmpTypeBase):
        '''Sets the XMP type value.
        
        :param key: The string representation of key that is identified with set value.
        :param value: The value to set to.'''
        ...
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        ...
    
    def set_created_date_str(self, created_date: str):
        '''Adds resource created date.
        
        :param created_date: Created date.'''
        ...
    
    def set_creator_tool(self, creator_tool: str):
        '''Sets the creator tool.
        
        :param creator_tool: Name of tool.'''
        ...
    
    def set_identifier(self, idenfifier: List[str]):
        '''Sets the identifier.
        
        :param idenfifier: The idenfifier.'''
        ...
    
    def set_label(self, label: str):
        '''Sets the label.
        
        :param label: The label.'''
        ...
    
    def set_metadata_date_str(self, metadata_date: str):
        '''Adds metadata last changed date.
        
        :param metadata_date: Metadata date.'''
        ...
    
    def set_modify_date_str(self, modified_date: str):
        '''Adds resource last modified date.
        
        :param modified_date: Last modified date.'''
        ...
    
    def set_rating(self, choise: int):
        '''Sets rating.
        
        :param choise: From -1 till 5'''
        ...
    
    @property
    def xml_namespace(self) -> str:
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    @classmethod
    @property
    def RATING_REJECTED(cls) -> int:
        ...
    
    @classmethod
    @property
    def RATING_MIN(cls) -> int:
        ...
    
    @classmethod
    @property
    def RATING_MAX(cls) -> int:
        ...
    
    ...

