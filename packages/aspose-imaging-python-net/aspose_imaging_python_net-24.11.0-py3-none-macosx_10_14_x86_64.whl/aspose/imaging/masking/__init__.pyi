"""The namespace handles ImageMasking processing."""
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

class IMaskingAsyncTask(aspose.imaging.asynctask.IAsyncTask):
    '''Represents the masking async task.'''
    
    def get_masking_result(self) -> aspose.imaging.masking.result.MaskingResult:
        '''Returns the result of masking operation
        
        :returns: The result of this task.'''
        ...
    
    def get_error(self) -> str:
        '''Returns an error of masking operation
        
        :returns: The task error.'''
        ...
    
    def run_async(self):
        '''Runs this task.'''
        ...
    
    def cancel(self):
        '''Cancels this task.
        The task is completed safely by the controlled stopping of the algorithm.'''
        ...
    
    def abort(self):
        '''Aborts this task.
        The task is completed immediately, with the risk of not freeing internal unmanaged resources.'''
        ...
    
    def wait_on_done(self):
        '''Waits until task is finished.'''
        ...
    
    @property
    def is_busy(self) -> bool:
        ...
    
    @property
    def is_canceled(self) -> bool:
        ...
    
    @property
    def is_faulted(self) -> bool:
        ...
    
    ...

class IMaskingSession:
    '''The masking session'''
    
    @overload
    def save(self, stream: io.RawIOBase):
        '''Save the session state to the specified stream.
        
        :param stream: The stream.'''
        ...
    
    @overload
    def save(self, file_path: str):
        '''Saves the session state to the specified file.
        
        :param file_path: The file path.'''
        ...
    
    def decompose(self) -> aspose.imaging.masking.result.MaskingResult:
        '''Performs first rough decompose operation
        
        :returns: Result of masking operation as array of segment image providers.'''
        ...
    
    def decompose_async(self) -> aspose.imaging.masking.IMaskingAsyncTask:
        '''Creates the asynchronous task which can perform first rough decompose operation
        
        :returns: The asynchronous decompose task'''
        ...
    
    def improve_decomposition(self, masking_arguments: aspose.imaging.masking.options.IMaskingArgs) -> aspose.imaging.masking.result.MaskingResult:
        '''Performs retraining decompose operation
        
        :param masking_arguments: The masking arguments.
        :returns: Result of masking operation as array of segment image providers.'''
        ...
    
    def improve_decomposition_async(self, masking_arguments: aspose.imaging.masking.options.IMaskingArgs) -> aspose.imaging.masking.IMaskingAsyncTask:
        '''Creates the asynchronous task which can perform retraining decompose operation
        
        :param masking_arguments: The masking arguments.
        :returns: The asynchronous decompose task'''
        ...
    
    ...

class ImageMasking:
    '''Provides image masking operations'''
    
    def __init__(self, source_image: aspose.imaging.RasterImage):
        '''Initializes a new instance of the  class.
        
        :param source_image: The source image.'''
        ...
    
    @overload
    def load_session(self, stream: io.RawIOBase) -> aspose.imaging.masking.IMaskingSession:
        '''Load the session from the specified stream.
        
        :param stream: The stream.
        :returns: the masking session which can perform retraining decompose operations.'''
        ...
    
    @overload
    def load_session(self, file_path: str) -> aspose.imaging.masking.IMaskingSession:
        '''Load the session from the specified file.
        
        :param file_path: The file path.
        :returns: the masking session which can perform retraining decompose operations.'''
        ...
    
    @staticmethod
    def apply_mask(target_image: aspose.imaging.RasterImage, mask: aspose.imaging.RasterImage, masking_options: aspose.imaging.masking.options.MaskingOptions):
        '''Applies the mask to specified source image.
        
        :param target_image: The target image.
        :param mask: The mask image to apply.
        :param masking_options: The masking options.'''
        ...
    
    def decompose(self, options: aspose.imaging.masking.options.MaskingOptions) -> aspose.imaging.masking.result.MaskingResult:
        '''Performs the decompose operation using specified masking options
        
        :param options: The masking options.
        :returns: Result of masking operation as array of segment image providers.'''
        ...
    
    def decompose_async(self, options: aspose.imaging.masking.options.MaskingOptions) -> aspose.imaging.masking.IMaskingAsyncTask:
        '''Creates the asynchronous decompose task using specified masking options.
        
        :param options: The masking options.
        :returns: The asynchronous decompose task'''
        ...
    
    def create_session(self, options: aspose.imaging.masking.options.MaskingOptions) -> aspose.imaging.masking.IMaskingSession:
        '''Creates the masking session which can perform retraining decompose operations.
        
        :param options: The options.
        :returns: the masking session which can perform retraining decompose operations.'''
        ...
    
    def load_session_from_stream(self, stream: io.RawIOBase) -> aspose.imaging.masking.IMaskingSession:
        '''Load the session from the specified stream.
        
        :param stream: The stream.
        :returns: the masking session which can perform retraining decompose operations.'''
        ...
    
    ...

