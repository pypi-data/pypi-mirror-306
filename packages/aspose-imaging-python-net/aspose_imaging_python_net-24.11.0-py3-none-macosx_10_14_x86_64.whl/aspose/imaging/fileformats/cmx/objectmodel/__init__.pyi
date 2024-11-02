"""The namespace handles Tiff file format processing."""
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

class CmxContainer(aspose.imaging.DisposableObject):
    '''the container for child elements.'''
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def elements(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.ICmxDocElement]:
        '''Gets the elements.'''
        ...
    
    ...

class CmxDocument:
    '''The CMX document.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def pages(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.CmxPage]:
        '''Gets the pages of current document.'''
        ...
    
    ...

class CmxGroup(CmxContainer):
    '''Group of'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def elements(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.ICmxDocElement]:
        '''Gets the elements.'''
        ...
    
    @property
    def bound_box(self) -> aspose.imaging.RectangleF:
        ...
    
    @bound_box.setter
    def bound_box(self, value : aspose.imaging.RectangleF):
        ...
    
    ...

class CmxLayer(CmxContainer):
    '''The graphic layer located on the page of the CMX document.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def elements(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.ICmxDocElement]:
        '''Gets the elements.'''
        ...
    
    @property
    def flags(self) -> int:
        '''Gets the flags.'''
        ...
    
    @flags.setter
    def flags(self, value : int):
        '''Sets the flags.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the layer.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name of the layer.'''
        ...
    
    @property
    def number(self) -> int:
        '''Gets the layer order number.'''
        ...
    
    @number.setter
    def number(self, value : int):
        '''Sets the layer order number.'''
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @classmethod
    @property
    def MASTER_DESKTOP_LAYER_NAME(cls) -> str:
        ...
    
    ...

class CmxObject(ICmxDocElement):
    '''Object containing information about the graphic element.'''
    
    def __init__(self):
        ...
    
    @property
    def fill_style(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxFillStyle:
        ...
    
    @fill_style.setter
    def fill_style(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxFillStyle):
        ...
    
    @property
    def outline(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxOutline:
        '''Gets the outline style.'''
        ...
    
    @outline.setter
    def outline(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxOutline):
        '''Sets the outline style.'''
        ...
    
    @property
    def object_spec(self) -> aspose.imaging.fileformats.cmx.objectmodel.specs.ICmxObjectSpec:
        ...
    
    @object_spec.setter
    def object_spec(self, value : aspose.imaging.fileformats.cmx.objectmodel.specs.ICmxObjectSpec):
        ...
    
    ...

class CmxPage(aspose.imaging.DisposableObject):
    '''The page of the CMX document.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def bound_box(self) -> aspose.imaging.RectangleF:
        ...
    
    @bound_box.setter
    def bound_box(self, value : aspose.imaging.RectangleF):
        ...
    
    @property
    def flags(self) -> int:
        '''Gets the flags.'''
        ...
    
    @flags.setter
    def flags(self, value : int):
        '''Sets the flags.'''
        ...
    
    @property
    def layers(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.CmxLayer]:
        '''Gets the page layers.'''
        ...
    
    @property
    def page_number(self) -> int:
        ...
    
    @page_number.setter
    def page_number(self, value : int):
        ...
    
    @property
    def width(self) -> float:
        '''Gets the page width.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the page width.'''
        ...
    
    @property
    def height(self) -> float:
        '''Gets the page height.'''
        ...
    
    @height.setter
    def height(self, value : float):
        '''Sets the page height.'''
        ...
    
    ...

class CmxProcedure(CmxContainer):
    '''The CMX procedure.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def elements(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.ICmxDocElement]:
        '''Gets the elements.'''
        ...
    
    @property
    def bound_box(self) -> aspose.imaging.RectangleF:
        ...
    
    @bound_box.setter
    def bound_box(self, value : aspose.imaging.RectangleF):
        ...
    
    ...

class ICmxContainer(ICmxDocElement):
    '''Defines the container for child elements.'''
    
    @property
    def elements(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.ICmxDocElement]:
        '''Gets the elements.'''
        ...
    
    ...

class ICmxDocElement:
    '''Defines the type of the child element of the CMX document.'''
    
    ...

