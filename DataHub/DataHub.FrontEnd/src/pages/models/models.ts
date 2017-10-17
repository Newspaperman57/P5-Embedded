import { Component } from '@angular/core';
import { Service } from '../../services/service';
import { ActivatedRoute } from '@angular/router';


@Component({
    templateUrl: './models.html'
})
export class Models {
    public modelTypes = [];
    public models = [];
    public loadingModels = true;
    public loadingModelTypes = true;
    constructor(
        private service: Service,
        private route: ActivatedRoute
    ) { }

    ngOnInit() {
      this.service.fetchModelTypes().then(
          data => {
              this.loadingModelTypes = false;
              if(data['Success'])
                this.modelTypes = data['Data'];
          }
      )
      this.service.fetchModels().then(
          data => {
              this.loadingModels = false;
              if(data['Success'])
                this.models = data['Data'];
          }
      )
    }
}