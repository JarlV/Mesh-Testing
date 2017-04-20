#include "nrf_drv_common.h"
#include "nrf_drv_ppi.h"
#include "nrf_drv_gpiote.h"
#include <nrf.h>

uint32_t err_code;
typedef uint32_t ret_code_t;
nrf_ppi_channel_t ppi_channel5;

// set ppi for end event and led 1 toggle
void set_ppi(int pin, uint32_t event, nrf_ppi_channel_t ppi_channel){
    ret_code_t c = nrf_drv_gpiote_init();
    
    //config event task
    nrf_drv_gpiote_out_config_t config = GPIOTE_CONFIG_OUT_TASK_TOGGLE(true);
    
    //config event task for radio
    err_code = nrf_drv_gpiote_out_init(pin, &config);
		
		err_code = nrf_drv_ppi_channel_alloc(&ppi_channel);
    APP_ERROR_CHECK(err_code);
    err_code = nrf_drv_ppi_channel_assign(ppi_channel,
										event,
										nrf_drv_gpiote_out_task_addr_get(pin));
    err_code = nrf_drv_ppi_channel_enable(ppi_channel);
		nrf_drv_gpiote_out_task_enable(pin);
}

int main(void){
	set_ppi(24, 			// LED 4
			0x40001108, 	// payload
			ppi_channel5);
}